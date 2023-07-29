#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 回溯Impala parquet表数据到ClickHouse replicated表  神策数据导clickhouse
:Author: 佳境Shmily
:Create Time: 2022/1/11 9:48
:File: impala_to_clickhouse
:Site: shmily-qjj.top
需要本地有impala-shell hdfs 及 clickhouse-client
运行在神策data01节点10.2.5.1
nohup python3.6 /home/sa_cluster/qjj/impala_p2_to_clickhouse.py >> /home/sa_cluster/qjj/impala_p2_to_clickhouse数据回溯.log &
若数据插入成功 不会在本地保留数据 不占磁盘 （失败会保留）
多线程操作  多任务同时进行
若要重新跑数据  需要对应修改如下参数  比如增量程序12号跑11号0点到12号0点的数据day=19004 那回溯程序就跑11号0点前的数据 参数如下：
    end_day = 19003
    end_data_time = "2022-01-11 00:00:00.000"
    相当于从day>= 19002 and day <= 19003 and time > '2022-01-10 00:00:00.000' and time <= '2022-01-11 00:00:00.000'开始 一天一天向前回溯
失败的情况排查：
除了cat /home/sa_cluster/qjj/impala_p2_to_clickhouse数据回溯.log | grep ERROR
还有可以查看{local_path}/failed_import_list 即/home/sa_cluster/qjj/data3/failed_import_list
first_day = 17500 表示17500之前的数据可以通过神策impala中的表default.event_ros_p2_export_16741_17000和default.event_ros_p2_export_17000_17500 两张表手动回溯  无需跑程序回溯（目前还未回溯这两表的数据）
"""
import datetime
import logging
import os
import threading
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
threadLock = threading.Lock()
try:
    import commands
except:
    import subprocess as commands


def execute_cmd(cmd, exit_on_failed=True):
    """
    执行linux shell命令
    :param cmd:
    :param exit_on_failed:
    :return:
    """
    stat, output = commands.getstatusoutput(cmd)
    if stat == 0:
        # logger.info(f"命令{cmd}执行成功")
        logger.info(f"命令{cmd.replace('''(event_id,month_id,week_id,user_id,distinct_id,time,p__app_version,p__carrier,p__city,p__country,p__ip,p__is_first_day,p__is_first_time,p__lib,p__lib_version,p__manufacturer,p__model,p__network_type,p__os,p__os_version,p__province,p__resume_from_background,p__screen_height,p__screen_name,p__screen_width,p__wifi,p_event_duration,p__title,p_app_channel,p_app_name,p_app_type,p_app_version,p_channel_code,p_create_time,p_cust_no,p_device_id,p_device_unique_id,p_enven_type,p_lbs,p_mac,p_message,p_network_type,p_operate_time,p_operation_sys,p_operation_sys_version,p_phone_marker,p_phone_model,p_phone_number,p_phone_operator,p_refer_cust,p_resolution,p_result,p_rowid,p_scene_type,p_smart_id,p_sub_app_channel,p_terminal_environment,p_token,p_user_agent_cust,p__browser,p__browser_version,p__device_id,p__is_login_id,p__track_signup_original_id,p_terminal_type,p_test_type,p_custno,p_tagiden,p_tagtime,p_tagtype,p_activityno,p_couponfacevalue,p_prizename,p_prizeunitprice,p_custiden,p_custtime,p_batchno,p_noticetopic,p_uploadtime,p_event_type,p_event_type_desc,p_scene_type_desc,p_sys,p_table_name,p_activity_no,p_batch_no,p_upload_time,p_businesscode,p_iscompare,p_coupontype,p__element_class_name,p__element_content,p__element_selector,p__element_type,p__latest_referrer,p__latest_referrer_host,p__latest_search_keyword,p__latest_traffic_source_type,p__referrer,p__referrer_host,p__url,p__url_path,p__element_target_url,p__element_id,p__element_name,p_applydate,p_bankcode,p_bankname,p_cardtype,p_idno,p_mobileno,p_schedulestatus,p_status,p_usrname,p_cardflag,p_bankauditdescription,p_audittime,p_body,p_type,p_testtype,p_companyname,p_amount,p_billstatus,p_cardno,p_day,p_sendtime,p_datatype,p_cardname,p_fee_rate_per_term,p_install_cnt,p_prod_sub_type,p_service_fee_rate,p_trans_amt,p_facevalue,p_itemno,p_face_value,p_item_no,p_service_fee_rates,_offset,p__kafka_offset,p_appname,p_update_datetime,p_capital_code,p_abnormal_status,p_buss_trans_date,p_open_bank_name,p_create_datetime,p_repay_type,p_repay_id,p_deal_time,p_ret_msg,p_scene_id,p_os_type,p_credit_id,p_approve_limit,p_response_info,p_bank_name,p_bank_no,p_channel,p_fee_amount,p_total_amount,p_payee_bank_name,p_discount_amount,p_payer_bank_name,p_bank_card_type,p_remark,p_trans_seqno,p_cap_sub_code,p_trans_date,p_cap_code,p_cap_name,p_repay_capital,p_pay_date,p_pbc_threshold,p_repayment_method,p_need_get_pbc_report,p_pbc_apply_type,p_cap_account,p_main_credit,p_loan_date,p_capital_name,p_month_rate,p_year_rate,p_credit_status,p_term,p_loan_id,p_pbc_id,p_cert_id,p_apply_type,p_valid_pattern,p_check_status,p_money,p_status_remark,p_approve_result,p_fee,p_third_cap_org_no,p_trans_code,p_send_channel,p_order_discount_amount,p_charge_type,p_prize_name,p_prize_provide_flag,p_trade_amount,p_failmsg,p_loanevent,p_createtime,p_scenetype,p_subappchannel,p_eventtype,p_decision,p_producttype,p_chanelcode,p_productname,p_createdate,p_apptype,p_updatetime,p_terminaltype,p_origflowno,p_inputrt3monthmaxplatform,p_updatedate,p_rsklogid,p_realtimedecision,p_appversion,p_appchannel,p_custname,p_success,p_rulecodes,p_inputtrxapplytime,p_errormsg,p_tdsuccess,p_tderrormsg,p_cust_org,p_custorg,p_message3,p_message1,p_message2,p_appkey,p_data_source,p_elapsed,p_status_msg,p_province,p_auth_result,p_mobile,p_canotp,p_ip,p_inputtransamt,p_risklevel,p_order_ret_msg,p_cancel_ret_msg,p_exec_ret_msg,p_action,p_channel_no,p_mobile_no,p_computer_host,p_maxentid,p_is_emulator,p_serial_no,p_ticket,p_gps_address,p_index,p_font,p_imei,p_intranel_ip,p_subscriber_i_d,p_product_name,p_font_size,p_reporteventname,p_black_box,p_reportmaxentid,p_longi_tude,p_product_type,p_lati_tude,p_browser_version,p_browser_type,p_sim_serial,p_app_key,p_event_status,p_pdf_id,p_standard_msg,p_biz_type,p_biz_sub_type,p_sms_status,p_return_msg,p_bank_code,p_channel_id,p_standard_code,p_verify_status,p_valid_method,p_merchant_id,p_return_code,p_step_status,p_notify_flag,p_trans_type,p_pay_amt,p_channelcode,p_from,p_operator,p_user_status,p_firsttrans,p_datefromtrxapplytime,p_policycode,p_nextstepcode,p_bscoreprob,p_bscoremodeltype,p_matrixinstallcnt,p_matrixtdlevel,p_matrixprodtype,p_matrixcustrisklevel,p_inputrt1monthmaxplatform,p_switchchannel,p_failchannel,p_num4,p_num2,p_num3,p_num1,p_loginrt3monthmaxplatform,p_loginrt1monthmaxplatform,p_credits,p_count,p_city,p_prodsubtype,p_level,p_path,p_fee_year_real_rate,p__app_state,p_code,p_srcsys,p_biztype,p_biztypedesc,p_channelcodedesc,p_times,p__receive_time,p_qd,p_errordesc,p_errorcode,p_company,p_orderid,p_origin_case_type,p_apply_channel,p_additional_credit,p_merchant_no,p__element_position,p_repay_amount,p_repay_start_time,p_repay_end_time,p_repay_cnt,p_transfer_amount,p_transfer_time,p_app_crashed_reason,p_origin_ny,p_apply_scene,p_apply_product,p_final_ny,p_account,p_end_time,p_paytype,p_downtime,p_insurenum,p_refund,p_number,p_register_channel,p_resulttype,p_transcode,p_repaymentmethod,p_uts_kudu_time,p_loan_type,p_trans_time,p_trans_amount,p_uts_mq_delay,p_info1,p_info4,p_info3,p_info2,p_channelagent,p_channelid,p_payvalue,p_member_order_type,p_own_vip_count,p_number1,p_number2,p__app_name,p__timezone_offset,p__app_id,p__lib_method,p__lib_plugin_version,p__app_remote_config,p_resource_scene,p_resource_list,p_resource_name,p_income,p_prizetypeno,p_uts_impala_ex_time,p__update_time,p_test_type1,p_key,day,event_bucket)''', '(...)')}执行成功")
        return True
    else:
        logger.error(output)
        logger.error(f"命令{cmd}执行失败 200s后重试")
        time.sleep(200)
        stat, output = commands.getstatusoutput(cmd)
        if stat == 0:
            logger.info(f"命令{cmd.replace('''(event_id,month_id,week_id,user_id,distinct_id,time,p__app_version,p__carrier,p__city,p__country,p__ip,p__is_first_day,p__is_first_time,p__lib,p__lib_version,p__manufacturer,p__model,p__network_type,p__os,p__os_version,p__province,p__resume_from_background,p__screen_height,p__screen_name,p__screen_width,p__wifi,p_event_duration,p__title,p_app_channel,p_app_name,p_app_type,p_app_version,p_channel_code,p_create_time,p_cust_no,p_device_id,p_device_unique_id,p_enven_type,p_lbs,p_mac,p_message,p_network_type,p_operate_time,p_operation_sys,p_operation_sys_version,p_phone_marker,p_phone_model,p_phone_number,p_phone_operator,p_refer_cust,p_resolution,p_result,p_rowid,p_scene_type,p_smart_id,p_sub_app_channel,p_terminal_environment,p_token,p_user_agent_cust,p__browser,p__browser_version,p__device_id,p__is_login_id,p__track_signup_original_id,p_terminal_type,p_test_type,p_custno,p_tagiden,p_tagtime,p_tagtype,p_activityno,p_couponfacevalue,p_prizename,p_prizeunitprice,p_custiden,p_custtime,p_batchno,p_noticetopic,p_uploadtime,p_event_type,p_event_type_desc,p_scene_type_desc,p_sys,p_table_name,p_activity_no,p_batch_no,p_upload_time,p_businesscode,p_iscompare,p_coupontype,p__element_class_name,p__element_content,p__element_selector,p__element_type,p__latest_referrer,p__latest_referrer_host,p__latest_search_keyword,p__latest_traffic_source_type,p__referrer,p__referrer_host,p__url,p__url_path,p__element_target_url,p__element_id,p__element_name,p_applydate,p_bankcode,p_bankname,p_cardtype,p_idno,p_mobileno,p_schedulestatus,p_status,p_usrname,p_cardflag,p_bankauditdescription,p_audittime,p_body,p_type,p_testtype,p_companyname,p_amount,p_billstatus,p_cardno,p_day,p_sendtime,p_datatype,p_cardname,p_fee_rate_per_term,p_install_cnt,p_prod_sub_type,p_service_fee_rate,p_trans_amt,p_facevalue,p_itemno,p_face_value,p_item_no,p_service_fee_rates,_offset,p__kafka_offset,p_appname,p_update_datetime,p_capital_code,p_abnormal_status,p_buss_trans_date,p_open_bank_name,p_create_datetime,p_repay_type,p_repay_id,p_deal_time,p_ret_msg,p_scene_id,p_os_type,p_credit_id,p_approve_limit,p_response_info,p_bank_name,p_bank_no,p_channel,p_fee_amount,p_total_amount,p_payee_bank_name,p_discount_amount,p_payer_bank_name,p_bank_card_type,p_remark,p_trans_seqno,p_cap_sub_code,p_trans_date,p_cap_code,p_cap_name,p_repay_capital,p_pay_date,p_pbc_threshold,p_repayment_method,p_need_get_pbc_report,p_pbc_apply_type,p_cap_account,p_main_credit,p_loan_date,p_capital_name,p_month_rate,p_year_rate,p_credit_status,p_term,p_loan_id,p_pbc_id,p_cert_id,p_apply_type,p_valid_pattern,p_check_status,p_money,p_status_remark,p_approve_result,p_fee,p_third_cap_org_no,p_trans_code,p_send_channel,p_order_discount_amount,p_charge_type,p_prize_name,p_prize_provide_flag,p_trade_amount,p_failmsg,p_loanevent,p_createtime,p_scenetype,p_subappchannel,p_eventtype,p_decision,p_producttype,p_chanelcode,p_productname,p_createdate,p_apptype,p_updatetime,p_terminaltype,p_origflowno,p_inputrt3monthmaxplatform,p_updatedate,p_rsklogid,p_realtimedecision,p_appversion,p_appchannel,p_custname,p_success,p_rulecodes,p_inputtrxapplytime,p_errormsg,p_tdsuccess,p_tderrormsg,p_cust_org,p_custorg,p_message3,p_message1,p_message2,p_appkey,p_data_source,p_elapsed,p_status_msg,p_province,p_auth_result,p_mobile,p_canotp,p_ip,p_inputtransamt,p_risklevel,p_order_ret_msg,p_cancel_ret_msg,p_exec_ret_msg,p_action,p_channel_no,p_mobile_no,p_computer_host,p_maxentid,p_is_emulator,p_serial_no,p_ticket,p_gps_address,p_index,p_font,p_imei,p_intranel_ip,p_subscriber_i_d,p_product_name,p_font_size,p_reporteventname,p_black_box,p_reportmaxentid,p_longi_tude,p_product_type,p_lati_tude,p_browser_version,p_browser_type,p_sim_serial,p_app_key,p_event_status,p_pdf_id,p_standard_msg,p_biz_type,p_biz_sub_type,p_sms_status,p_return_msg,p_bank_code,p_channel_id,p_standard_code,p_verify_status,p_valid_method,p_merchant_id,p_return_code,p_step_status,p_notify_flag,p_trans_type,p_pay_amt,p_channelcode,p_from,p_operator,p_user_status,p_firsttrans,p_datefromtrxapplytime,p_policycode,p_nextstepcode,p_bscoreprob,p_bscoremodeltype,p_matrixinstallcnt,p_matrixtdlevel,p_matrixprodtype,p_matrixcustrisklevel,p_inputrt1monthmaxplatform,p_switchchannel,p_failchannel,p_num4,p_num2,p_num3,p_num1,p_loginrt3monthmaxplatform,p_loginrt1monthmaxplatform,p_credits,p_count,p_city,p_prodsubtype,p_level,p_path,p_fee_year_real_rate,p__app_state,p_code,p_srcsys,p_biztype,p_biztypedesc,p_channelcodedesc,p_times,p__receive_time,p_qd,p_errordesc,p_errorcode,p_company,p_orderid,p_origin_case_type,p_apply_channel,p_additional_credit,p_merchant_no,p__element_position,p_repay_amount,p_repay_start_time,p_repay_end_time,p_repay_cnt,p_transfer_amount,p_transfer_time,p_app_crashed_reason,p_origin_ny,p_apply_scene,p_apply_product,p_final_ny,p_account,p_end_time,p_paytype,p_downtime,p_insurenum,p_refund,p_number,p_register_channel,p_resulttype,p_transcode,p_repaymentmethod,p_uts_kudu_time,p_loan_type,p_trans_time,p_trans_amount,p_uts_mq_delay,p_info1,p_info4,p_info3,p_info2,p_channelagent,p_channelid,p_payvalue,p_member_order_type,p_own_vip_count,p_number1,p_number2,p__app_name,p__timezone_offset,p__app_id,p__lib_method,p__lib_plugin_version,p__app_remote_config,p_resource_scene,p_resource_list,p_resource_name,p_income,p_prizetypeno,p_uts_impala_ex_time,p__update_time,p_test_type1,p_key,day,event_bucket)''', '(...)')}执行成功")
            return True
        else:
            logger.error(output)
            logger.error(f"命令{cmd}执行失败")
            if exit_on_failed:
                # exit()
                # os._exit()用于退出当前进程中的主线程
                # sys.exit()用于退出当前线程  只退出当前线程会造成建临时表线程关闭，后续线程因没有建完的临时表而一直等待
                os._exit(1)
            else:
                return False


def create_temp_table(impalad_ip, impalad_port, sqls):
    """
    # 创建临时表
    :param impalad_ip:
    :param impalad_port:
    :param sqls:
    :return:
    """
    cmd = f"impala-shell -i {impalad_ip}:{impalad_port} -q \"set PARQUET_FILE_SIZE=128m;{sqls}\""
    cnt = 0
    while cnt <= 9:
        if execute_cmd(cmd, False):
            return
        else:
            logger.warning("create_temp_table 开始重试1次")
            cnt += 1
    logger.error(f"{cmd} 运行10次仍然失败 记录到文件")
    threadLock.acquire()
    f = open(f"{local_path}/failed_import_list", 'a')
    f.write(cmd + "\n")
    f.close()
    threadLock.release()


def get_data(hdfs_path, local_path):
    """
    表数据文件下载
    :param hdfs_path:
    :param local_path:
    :return:
    """
    cmd = f"mkdir -p {local_path} ; hdfs dfs -get {hdfs_path} {local_path}"
    if not execute_cmd(cmd, False):
        threadLock.acquire()
        f = open(f"{local_path}/failed_import_list", 'a')
        f.write(cmd + "\n")
        f.close()
        threadLock.release()


def load_data(clickhouse_server, clickhouse_cli_port, clickhouse_table, data_files, data_format='Parquet'):
    """
    # ClickHouse Load数据文件
    :param clickhouse_server:
    :param clickhouse_cli_port:
    :param clickhouse_table:
    :param data_files:
    :param data_format:
    :return:
    """
    all_success_flag = True
    for root, dirs, files in os.walk(data_files, topdown=False):
        files = list(filter(lambda x: x.endswith(".parq"), files))
        for name in files:
            parquet_file_name = os.path.join(root, name)
            cmd = f'''clickhouse-client -h {clickhouse_server} --port {clickhouse_cli_port} --input_format_allow_errors_num 8 --max_memory_usage=100000000000 --max_insert_threads=32 --query="INSERT INTO {clickhouse_table}(event_id,month_id,week_id,user_id,distinct_id,time,p__app_version,p__carrier,p__city,p__country,p__ip,p__is_first_day,p__is_first_time,p__lib,p__lib_version,p__manufacturer,p__model,p__network_type,p__os,p__os_version,p__province,p__resume_from_background,p__screen_height,p__screen_name,p__screen_width,p__wifi,p_event_duration,p__title,p_app_channel,p_app_name,p_app_type,p_app_version,p_channel_code,p_create_time,p_cust_no,p_device_id,p_device_unique_id,p_enven_type,p_lbs,p_mac,p_message,p_network_type,p_operate_time,p_operation_sys,p_operation_sys_version,p_phone_marker,p_phone_model,p_phone_number,p_phone_operator,p_refer_cust,p_resolution,p_result,p_rowid,p_scene_type,p_smart_id,p_sub_app_channel,p_terminal_environment,p_token,p_user_agent_cust,p__browser,p__browser_version,p__device_id,p__is_login_id,p__track_signup_original_id,p_terminal_type,p_test_type,p_custno,p_tagiden,p_tagtime,p_tagtype,p_activityno,p_couponfacevalue,p_prizename,p_prizeunitprice,p_custiden,p_custtime,p_batchno,p_noticetopic,p_uploadtime,p_event_type,p_event_type_desc,p_scene_type_desc,p_sys,p_table_name,p_activity_no,p_batch_no,p_upload_time,p_businesscode,p_iscompare,p_coupontype,p__element_class_name,p__element_content,p__element_selector,p__element_type,p__latest_referrer,p__latest_referrer_host,p__latest_search_keyword,p__latest_traffic_source_type,p__referrer,p__referrer_host,p__url,p__url_path,p__element_target_url,p__element_id,p__element_name,p_applydate,p_bankcode,p_bankname,p_cardtype,p_idno,p_mobileno,p_schedulestatus,p_status,p_usrname,p_cardflag,p_bankauditdescription,p_audittime,p_body,p_type,p_testtype,p_companyname,p_amount,p_billstatus,p_cardno,p_day,p_sendtime,p_datatype,p_cardname,p_fee_rate_per_term,p_install_cnt,p_prod_sub_type,p_service_fee_rate,p_trans_amt,p_facevalue,p_itemno,p_face_value,p_item_no,p_service_fee_rates,_offset,p__kafka_offset,p_appname,p_update_datetime,p_capital_code,p_abnormal_status,p_buss_trans_date,p_open_bank_name,p_create_datetime,p_repay_type,p_repay_id,p_deal_time,p_ret_msg,p_scene_id,p_os_type,p_credit_id,p_approve_limit,p_response_info,p_bank_name,p_bank_no,p_channel,p_fee_amount,p_total_amount,p_payee_bank_name,p_discount_amount,p_payer_bank_name,p_bank_card_type,p_remark,p_trans_seqno,p_cap_sub_code,p_trans_date,p_cap_code,p_cap_name,p_repay_capital,p_pay_date,p_pbc_threshold,p_repayment_method,p_need_get_pbc_report,p_pbc_apply_type,p_cap_account,p_main_credit,p_loan_date,p_capital_name,p_month_rate,p_year_rate,p_credit_status,p_term,p_loan_id,p_pbc_id,p_cert_id,p_apply_type,p_valid_pattern,p_check_status,p_money,p_status_remark,p_approve_result,p_fee,p_third_cap_org_no,p_trans_code,p_send_channel,p_order_discount_amount,p_charge_type,p_prize_name,p_prize_provide_flag,p_trade_amount,p_failmsg,p_loanevent,p_createtime,p_scenetype,p_subappchannel,p_eventtype,p_decision,p_producttype,p_chanelcode,p_productname,p_createdate,p_apptype,p_updatetime,p_terminaltype,p_origflowno,p_inputrt3monthmaxplatform,p_updatedate,p_rsklogid,p_realtimedecision,p_appversion,p_appchannel,p_custname,p_success,p_rulecodes,p_inputtrxapplytime,p_errormsg,p_tdsuccess,p_tderrormsg,p_cust_org,p_custorg,p_message3,p_message1,p_message2,p_appkey,p_data_source,p_elapsed,p_status_msg,p_province,p_auth_result,p_mobile,p_canotp,p_ip,p_inputtransamt,p_risklevel,p_order_ret_msg,p_cancel_ret_msg,p_exec_ret_msg,p_action,p_channel_no,p_mobile_no,p_computer_host,p_maxentid,p_is_emulator,p_serial_no,p_ticket,p_gps_address,p_index,p_font,p_imei,p_intranel_ip,p_subscriber_i_d,p_product_name,p_font_size,p_reporteventname,p_black_box,p_reportmaxentid,p_longi_tude,p_product_type,p_lati_tude,p_browser_version,p_browser_type,p_sim_serial,p_app_key,p_event_status,p_pdf_id,p_standard_msg,p_biz_type,p_biz_sub_type,p_sms_status,p_return_msg,p_bank_code,p_channel_id,p_standard_code,p_verify_status,p_valid_method,p_merchant_id,p_return_code,p_step_status,p_notify_flag,p_trans_type,p_pay_amt,p_channelcode,p_from,p_operator,p_user_status,p_firsttrans,p_datefromtrxapplytime,p_policycode,p_nextstepcode,p_bscoreprob,p_bscoremodeltype,p_matrixinstallcnt,p_matrixtdlevel,p_matrixprodtype,p_matrixcustrisklevel,p_inputrt1monthmaxplatform,p_switchchannel,p_failchannel,p_num4,p_num2,p_num3,p_num1,p_loginrt3monthmaxplatform,p_loginrt1monthmaxplatform,p_credits,p_count,p_city,p_prodsubtype,p_level,p_path,p_fee_year_real_rate,p__app_state,p_code,p_srcsys,p_biztype,p_biztypedesc,p_channelcodedesc,p_times,p__receive_time,p_qd,p_errordesc,p_errorcode,p_company,p_orderid,p_origin_case_type,p_apply_channel,p_additional_credit,p_merchant_no,p__element_position,p_repay_amount,p_repay_start_time,p_repay_end_time,p_repay_cnt,p_transfer_amount,p_transfer_time,p_app_crashed_reason,p_origin_ny,p_apply_scene,p_apply_product,p_final_ny,p_account,p_end_time,p_paytype,p_downtime,p_insurenum,p_refund,p_number,p_register_channel,p_resulttype,p_transcode,p_repaymentmethod,p_uts_kudu_time,p_loan_type,p_trans_time,p_trans_amount,p_uts_mq_delay,p_info1,p_info4,p_info3,p_info2,p_channelagent,p_channelid,p_payvalue,p_member_order_type,p_own_vip_count,p_number1,p_number2,p__app_name,p__timezone_offset,p__app_id,p__lib_method,p__lib_plugin_version,p__app_remote_config,p_resource_scene,p_resource_list,p_resource_name,p_income,p_prizetypeno,p_uts_impala_ex_time,p__update_time,p_test_type1,p_key,day,event_bucket) FORMAT {data_format}" < {parquet_file_name}'''
            if not execute_cmd(cmd, False):
                all_success_flag = False
                threadLock.acquire()
                f = open(f"{local_path}/failed_import_list", 'a')
                f.write(cmd + "\n")
                f.close()
                threadLock.release()
                logger.error(f"load_data中数据文件{parquet_file_name}导入失败")
    return all_success_flag


def clear_data(files_path):
    """
    数据目录清理
    :param files_path:
    :return:
    """
    if not os.path.exists(files_path):
        logger.warning(f"Path {files_path} dose not exists.")
        return
    for root, dirs, files in os.walk(files_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(files_path)


def run_i2c_threading(full_tasks):
    """
    多线程执行
    :param full_tasks:
    :return:
    """
    logger.info("======开始多线程模式数据抽取模式======")
    threads = []
    need_run_tasks = full_tasks.copy()
    tmp_table_done_queue = []
    get_data_done_queue = []
    all_done_list = []

    def tmp_table_create():
        while 1:
            if len(need_run_tasks) != 0:
                st = time.time()
                task_name = need_run_tasks.pop(0)
                logger.info(f"tmp_table_create 开始创建临时表:{task_name}")
                start_time, end_time, day_partition = task_name
                # time.sleep(10)
                sqls = f"""drop table if exists default.event_ros_p2_{day_partition};set PARQUET_FILE_SIZE=128m;create table default.event_ros_p2_{day_partition} stored as parquet as select event_id,month_id,week_id,user_id,distinct_id,hours_sub(time,8) as time,p__app_version,p__carrier,p__city,p__country,p__ip,p__is_first_day,p__is_first_time,p__lib,p__lib_version,p__manufacturer,p__model,p__network_type,p__os,p__os_version,p__province,p__resume_from_background,p__screen_height,p__screen_name,p__screen_width,p__wifi,p_event_duration,p__title,p_app_channel,p_app_name,p_app_type,p_app_version,p_channel_code,p_create_time,p_cust_no,p_device_id,p_device_unique_id,p_enven_type,p_lbs,p_mac,p_message,p_network_type,p_operate_time,p_operation_sys,p_operation_sys_version,p_phone_marker,p_phone_model,p_phone_number,p_phone_operator,p_refer_cust,p_resolution,p_result,p_rowid,p_scene_type,p_smart_id,p_sub_app_channel,p_terminal_environment,p_token,p_user_agent_cust,p__browser,p__browser_version,p__device_id,p__is_login_id,p__track_signup_original_id,p_terminal_type,p_test_type,p_custno,p_tagiden,p_tagtime,p_tagtype,p_activityno,p_couponfacevalue,p_prizename,p_prizeunitprice,p_custiden,p_custtime,p_batchno,p_noticetopic,p_uploadtime,p_event_type,p_event_type_desc,p_scene_type_desc,p_sys,p_table_name,p_activity_no,p_batch_no,p_upload_time,p_businesscode,p_iscompare,p_coupontype,p__element_class_name,p__element_content,p__element_selector,p__element_type,p__latest_referrer,p__latest_referrer_host,p__latest_search_keyword,p__latest_traffic_source_type,p__referrer,p__referrer_host,p__url,p__url_path,p__element_target_url,p__element_id,p__element_name,p_applydate,p_bankcode,p_bankname,p_cardtype,p_idno,p_mobileno,p_schedulestatus,p_status,p_usrname,p_cardflag,p_bankauditdescription,p_audittime,p_body,p_type,p_testtype,p_companyname,p_amount,p_billstatus,p_cardno,p_day,p_sendtime,p_datatype,p_cardname,p_fee_rate_per_term,p_install_cnt,p_prod_sub_type,p_service_fee_rate,p_trans_amt,p_facevalue,p_itemno,p_face_value,p_item_no,p_service_fee_rates,_offset,p__kafka_offset,p_appname,p_update_datetime,p_capital_code,p_abnormal_status,p_buss_trans_date,p_open_bank_name,p_create_datetime,p_repay_type,p_repay_id,p_deal_time,p_ret_msg,p_scene_id,p_os_type,p_credit_id,p_approve_limit,p_response_info,p_bank_name,p_bank_no,p_channel,p_fee_amount,p_total_amount,p_payee_bank_name,p_discount_amount,p_payer_bank_name,p_bank_card_type,p_remark,p_trans_seqno,p_cap_sub_code,p_trans_date,p_cap_code,p_cap_name,p_repay_capital,p_pay_date,p_pbc_threshold,p_repayment_method,p_need_get_pbc_report,p_pbc_apply_type,p_cap_account,p_main_credit,p_loan_date,p_capital_name,p_month_rate,p_year_rate,p_credit_status,p_term,p_loan_id,p_pbc_id,p_cert_id,p_apply_type,p_valid_pattern,p_check_status,p_money,p_status_remark,p_approve_result,p_fee,p_third_cap_org_no,p_trans_code,p_send_channel,p_order_discount_amount,p_charge_type,p_prize_name,p_prize_provide_flag,p_trade_amount,p_failmsg,p_loanevent,p_createtime,p_scenetype,p_subappchannel,p_eventtype,p_decision,p_producttype,p_chanelcode,p_productname,p_createdate,p_apptype,p_updatetime,p_terminaltype,p_origflowno,p_inputrt3monthmaxplatform,p_updatedate,p_rsklogid,p_realtimedecision,p_appversion,p_appchannel,p_custname,p_success,p_rulecodes,p_inputtrxapplytime,p_errormsg,p_tdsuccess,p_tderrormsg,p_cust_org,p_custorg,p_message3,p_message1,p_message2,p_appkey,p_data_source,p_elapsed,p_status_msg,p_province,p_auth_result,p_mobile,p_canotp,p_ip,p_inputtransamt,p_risklevel,p_order_ret_msg,p_cancel_ret_msg,p_exec_ret_msg,p_action,p_channel_no,p_mobile_no,p_computer_host,p_maxentid,p_is_emulator,p_serial_no,p_ticket,p_gps_address,p_index,p_font,p_imei,p_intranel_ip,p_subscriber_i_d,p_product_name,p_font_size,p_reporteventname,p_black_box,p_reportmaxentid,p_longi_tude,p_product_type,p_lati_tude,p_browser_version,p_browser_type,p_sim_serial,p_app_key,p_event_status,p_pdf_id,p_standard_msg,p_biz_type,p_biz_sub_type,p_sms_status,p_return_msg,p_bank_code,p_channel_id,p_standard_code,p_verify_status,p_valid_method,p_merchant_id,p_return_code,p_step_status,p_notify_flag,p_trans_type,p_pay_amt,p_channelcode,p_from,p_operator,p_user_status,p_firsttrans,p_datefromtrxapplytime,p_policycode,p_nextstepcode,p_bscoreprob,p_bscoremodeltype,p_matrixinstallcnt,p_matrixtdlevel,p_matrixprodtype,p_matrixcustrisklevel,p_inputrt1monthmaxplatform,p_switchchannel,p_failchannel,p_num4,p_num2,p_num3,p_num1,p_loginrt3monthmaxplatform,p_loginrt1monthmaxplatform,p_credits,p_count,p_city,p_prodsubtype,p_level,p_path,p_fee_year_real_rate,p__app_state,p_code,p_srcsys,p_biztype,p_biztypedesc,p_channelcodedesc,p_times,p__receive_time,p_qd,p_errordesc,p_errorcode,p_company,p_orderid,p_origin_case_type,p_apply_channel,p_additional_credit,p_merchant_no,p__element_position,p_repay_amount,p_repay_start_time,p_repay_end_time,p_repay_cnt,p_transfer_amount,p_transfer_time,p_app_crashed_reason,p_origin_ny,p_apply_scene,p_apply_product,p_final_ny,p_account,p_end_time,p_paytype,p_downtime,p_insurenum,p_refund,p_number,p_register_channel,p_resulttype,p_transcode,p_repaymentmethod,p_uts_kudu_time,p_loan_type,p_trans_time,p_trans_amount,p_uts_mq_delay,p_info1,p_info4,p_info3,p_info2,p_channelagent,p_channelid,p_payvalue,p_member_order_type,p_own_vip_count,p_number1,p_number2,p__app_name,p__timezone_offset,p__app_id,p__lib_method,p__lib_plugin_version,p__app_remote_config,p_resource_scene,p_resource_list,p_resource_name,p_income,p_prizetypeno,p_uts_impala_ex_time,p__update_time,p_test_type1,p_key,day,event_bucket from rawdata.event_ros_p2 where day = {day_partition} and time >= '{start_time}' and time < '{end_time}'"""
                create_temp_table(impalad_ip, impalad_port, sqls)
                tmp_table_done_queue.append(task_name)  # 加入已完成临时表创建的队列
                logger.info(f"tmp_table_create 完成创建临时表:{task_name} 耗时{time.time() - st}")
            else:
                logger.info(f"===========所有tmp_table_create任务完成===========")
                return

    def getting_data():
        while True:
            if len(tmp_table_done_queue) != 0:
                st = time.time()
                task_name = tmp_table_done_queue.pop(0)
                start_time, end_time, day_partition = task_name
                logger.info(f"getting_data 开始下载数据:{task_name}")
                # time.sleep(5)
                get_data(f"/user/hive/warehouse/event_ros_p2_{day_partition}", local_path)
                get_data_done_queue.append(task_name)
                logger.info(f"getting_data 完成下载数据:{task_name} 耗时{time.time() - st}")
            elif len(full_tasks) != len(all_done_list):
                logger.info(f"need_run_tasks:{len(need_run_tasks)} tmp_table:{len(tmp_table_done_queue)} getting_data:{len(get_data_done_queue)} all_done:{len(all_done_list)} 等待getting_data")
                time.sleep(60)
            else:
                logger.info("===========所有getting_data任务完成===========")
                return

    def loading_data_to_local_table():
        """
        加载所有文件到clickhouse本地表
        :return:
        """
        clickhouse_server = "10.2.5.231"
        clickhouse_cli_port = 9030
        while 1:
            if len(get_data_done_queue) != 0:
                st = time.time()
                task_name = get_data_done_queue.pop(0)
                start_time, end_time, day_partition = task_name
                logger.info(f"loading_data_to_local_table 开始加载文件到ClickHouse:{task_name}")
                if load_data(clickhouse_server, clickhouse_cli_port, "default.event_ros_p2", f"{local_path}/event_ros_p2_{day_partition}/"):
                    logger.info(f"loading_data_to_local_table 完成加载文件到ClickHouse:{task_name} 耗时{time.time() - st}")
                    clear_data(f"{local_path}/event_ros_p2_{day_partition}")
                else:
                    logger.error(f"loading_data_to_local_table 加载文件到ClickHouse有部分失败:{task_name} 耗时{time.time() - st}")
                all_done_list.append(task_name)
                logger.info(f"已完成 where day = {day_partition} and time >= '{start_time}' and time < '{end_time}' 数据的导入")
            elif len(full_tasks) != len(all_done_list):
                logger.info(f"need_run_tasks:{len(need_run_tasks)} tmp_table:{len(tmp_table_done_queue)} getting_data:{len(get_data_done_queue)} all_done:{len(all_done_list)} 等待loading_data")
                time.sleep(30)
            else:
                logger.info("===========所有loading_data任务完成===========")
                return

    def loading_data():
        """
        文件分为多份 相当于多个shard 分别load到clickhouse分布式表的本地表及其副本
        :return:
        """
        # 导入数据到本地表及副本
        while True:
            if len(get_data_done_queue) != 0:
                st = time.time()
                task_name = get_data_done_queue.pop(0)
                start_time, end_time, day_partition = task_name
                logger.info(f"loading_data 开始加载文件到ClickHouse分布式表:{task_name}")

                need_loading_files = f"{local_path}/event_ros_p2_{day_partition}/"
                if not os.path.exists(need_loading_files):
                    logger.warning(f"Path {need_loading_files} dose not exists.")
                    return
                # 分发文件为5份
                execute_cmd(f"mkdir -p {need_loading_files}/part1")
                execute_cmd(f"mkdir -p {need_loading_files}/part2")
                execute_cmd(f"mkdir -p {need_loading_files}/part3")
                execute_cmd(f"mkdir -p {need_loading_files}/part4")
                execute_cmd(f"mkdir -p {need_loading_files}/part5")

                # for root, dirs, files in os.walk(need_loading_files, topdown=False):
                #     part_count = math.floor(len(files) / 5)
                #     fcnt = 0
                #     dcnt = 1
                #     for name in files:
                #         file_name = os.path.join(root, name)
                #         execute_cmd(f"mv {file_name} {need_loading_files}/part{dcnt}/", False)
                #         fcnt += 1
                #         if fcnt == part_count and dcnt < 5:
                #             dcnt += 1
                #             fcnt = 0

                for root, dirs, files in os.walk(need_loading_files, topdown=False):
                    cfc = 0
                    files = list(filter(lambda x: x.endswith(".parq"), files))
                    for name in files:
                        file_name = os.path.join(root, name)
                        if cfc % 5 == 0:
                            execute_cmd(f"mv {file_name} {need_loading_files}/part1/")
                        elif cfc % 5 == 1:
                            execute_cmd(f"mv {file_name} {need_loading_files}/part2/")
                        elif cfc % 5 == 2:
                            execute_cmd(f"mv {file_name} {need_loading_files}/part3/")
                        elif cfc % 5 == 3:
                            execute_cmd(f"mv {file_name} {need_loading_files}/part4/")
                        else:
                            execute_cmd(f"mv {file_name} {need_loading_files}/part5/")
                        cfc = cfc + 1

                def load_to_local_table(clickhouse_server_1, clickhouse_cli_port, local_table_1, files_path):
                    if not load_data(clickhouse_server_1, clickhouse_cli_port, local_table_1, files_path):
                        logger.error("load_to_local_table 同一分片的部分数据文件导入ClickHouse失败")
                    else:
                        logger.info(f"load_to_local_table 成功 清理数据{files_path}")
                        # 如果load全部成功就清理掉目录
                        clear_data(files_path)

                thread_a = threading.Thread(target=load_to_local_table, args=("10.2.5.230", "9030", "db01.event_ros_p2_local_replicated", f"{need_loading_files}/part1/"))
                thread_b = threading.Thread(target=load_to_local_table, args=("10.2.5.231", "9030", "db01.event_ros_p2_local_replicated", f"{need_loading_files}/part2/"))
                thread_c = threading.Thread(target=load_to_local_table, args=("10.2.5.232", "9030", "db01.event_ros_p2_local_replicated", f"{need_loading_files}/part3/"))
                thread_d = threading.Thread(target=load_to_local_table, args=("10.2.5.233", "9030", "db01.event_ros_p2_local_replicated", f"{need_loading_files}/part4/"))
                thread_e = threading.Thread(target=load_to_local_table, args=("10.2.5.234", "9030", "db01.event_ros_p2_local_replicated", f"{need_loading_files}/part5/"))
                insert_threads = []
                thread_a.start()
                thread_b.start()
                thread_c.start()
                thread_d.start()
                thread_e.start()
                insert_threads.append(thread_a)
                insert_threads.append(thread_b)
                insert_threads.append(thread_c)
                insert_threads.append(thread_d)
                insert_threads.append(thread_e)
                for th in insert_threads:
                    th.join()
                logger.info(f"loading_data 完成加载文件到ClickHouse分布式表:{task_name} 耗时{time.time() - st}")
                all_done_list.append(task_name)
                logger.info(f"已完成 day = {day_partition} and time >= '{start_time}' and time < '{end_time}' 数据的导入")
            elif len(full_tasks) != len(all_done_list):
                logger.info(f"need_run_tasks:{len(need_run_tasks)} tmp_table:{len(tmp_table_done_queue)} getting_data:{len(get_data_done_queue)} all_done:{len(all_done_list)} 等待loading_data")
                time.sleep(60)
            else:
                logger.info("===========所有loading_data任务完成===========")
                return

    thread1 = threading.Thread(target=tmp_table_create, args=())
    thread2 = threading.Thread(target=getting_data, args=())
    thread3 = threading.Thread(target=loading_data, args=())
    thread1.start()
    thread2.start()
    thread3.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    for t in threads:
        t.join()
    logger.info(f"need_run_tasks:{need_run_tasks}")
    logger.info(f"tmp_table_done_queue:{tmp_table_done_queue}")
    logger.info(f"get_data_done_queue:{get_data_done_queue}")
    logger.info(f"all_done_list:{all_done_list}")
    logger.info("======多线程模式数据抽取完成======")


# # 单线程执行
# def run_i2c(full_tasks):
#     clickhouse_server = "10.2.5.231"
#     clickhouse_cli_port = 9030
#     for task in full_tasks:
#         st = time.time()
#         start_time, end_time, day_partition = task
#         logger.info(f"===开始单线程执行数据抽取任务{task}===")
#         sqls = f"""drop table if exists event_ros_p2_{sd}_{ed};set PARQUET_FILE_SIZE=128m;create table event_ros_p2_{sd}_{ed} stored as parquet as select * from rawdata.event_ros_p2 where day>= {sd} and day <= {ed} and time > '{start_time}' and time <= '{end_time}'"""
#         create_temp_table(impalad_ip, impalad_port, sqls)
#         get_data(f"/user/hive/warehouse/event_ros_p2_{sd}_{ed}", local_path)
#         load_data(clickhouse_server, clickhouse_cli_port, "default.event_ros_p2", f"{local_path}/event_ros_p2_{sd}_{ed}/")
#         clear_data(f"{local_path}/event_ros_p2_{sd}_{ed}")
#         logger.info(f"已完成 day>= {sd} and day <= {ed} and time > '{start_time}' and time <= '{end_time}' 数据的导入 总耗时{time.time() - st}秒")
#     logger.info("All Done")


if __name__ == '__main__':
    # day=18998 分区是2022-01-06 00:00:00 ~ 2022-01-07 00:00:00（不含）的数据
    # day=18999包含了2022-01-07 00:00:00.000的数据 所以每次扫描相邻两个分区即可 eg: where day >= 18998 and day <= 18999 and time > "2022-01-06 00:00:00.000000000" and time <= "2022-01-07 00:00:00.000000000";

    # 改成左闭右开
    # eg: where day=19015 and time >= '2022-01-23 00:00:00.000' and time < '2022-01-24 00:00:00.000'
    end_day = 19015  # 分区19015 数据1.23 00:00:00.000~1.23 23:59:59.999 即小于1月24 00:00:00.000
    end_data_time = "2022-01-24 00:00:00.000"
    first_day = 16741   # 包含17500的数据  17500之前的数据已手动导入
    impalad_ip = "10.2.5.3"
    impalad_port = 21000
    local_path = "/home/sa_cluster/qjj/data3/replicated"
    total_tasks = []
    for delta_day in range(end_day - first_day):
        end_time = (datetime.datetime.strptime(end_data_time, '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=-delta_day)).strftime("%Y-%m-%d 00:00:00.000000000")
        start_time = (datetime.datetime.strptime(end_data_time, '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=-delta_day-1)).strftime("%Y-%m-%d 00:00:00.000000000")
        day_partition = end_day - delta_day
        # print(start_time, end_time, day_partition)
        total_tasks.append([start_time, end_time, day_partition])

    # Multi Thread
    run_i2c_threading(total_tasks)

    # Single Thread
    # run_i2c(total_tasks)

