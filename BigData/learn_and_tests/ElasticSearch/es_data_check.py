#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
from functools import reduce

import requests
import time
from requests.auth import HTTPBasicAuth
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


OLD_ES_ADDR = "http://old_es_ip:9200"
NEW_ES_ADDR = "http://new_es_ip:9200"
OLD_ES_AUTH = HTTPBasicAuth('elastic', '111111')
NEW_ES_AUTH = HTTPBasicAuth('elastic', '222222')
OLD_ES_INDEX = "index_name_in_old_cluster"
NEW_ES_INDEX = "index_name_in_new_cluster"

"""
ES新旧集群 某个index数据对比
"""

def query_es(api_path, json_data_str, es_addr, es_auth, index_name):
    url = f"""{es_addr}/{index_name}/{api_path}""" if index_name != "" else f"""{es_addr}/{api_path}"""
    res = requests.get(url, data=json_data_str, auth=es_auth, headers={'Content-type': 'application/json'})
    if res.status_code == 200:
        return res.json()
    else:
        logger.error("查询es失败，err:\n" + res.text)


def get_doc_by_userid(es_addr, es_auth, index_name, user_id):
    logger.debug("查询userid %s 对应的文档" % user_id)
    json_data_str = """
    {
    "query":{
        "match_phrase": {
            "userid":{
                "query": "%s"
            }
        }
    }
}
    """ % user_id

    try:
        return query_es("_search", json_data_str, es_addr, es_auth, index_name) \
            .get('hits').get('hits')[0].get('_source')
    except:
        return None


def check_data_consistency(old_es_data, new_es_data):
    st = time.time()
    old_es_hits = reduce(lambda x, y: dict(x, **y), map(lambda x: {str(x.get('_source').get('userid')): x.get('_source')}, old_es_data.get('hits').get('hits')))
    new_es_hits = reduce(lambda x, y: dict(x, **y), map(lambda x: {str(x.get('_source').get('userid')): x.get('_source')}, new_es_data.get('hits').get('hits')))

    # 不一致场景统计
    inconsistent_dict = {}

    total_cnt = len(old_es_hits.keys())
    if total_cnt == 0:
        return
    consistence_cnt = 0
    for key in old_es_hits.keys():
        old_es_doc: dict = old_es_hits.get(key)
        # sort merge 方式可能存在每批次有不同user关联不上，对这些user做单独查询
        new_es_doc: dict = new_es_hits.get(key) \
            if new_es_hits.get(key) \
            else get_doc_by_userid(NEW_ES_ADDR, NEW_ES_AUTH, NEW_ES_INDEX, old_es_doc.get('userid'))


        old_es_doc.pop('updateTime')
        new_es_doc.pop('updateTime')

        if old_es_doc.items() <= new_es_doc.items():
            # old_es_doc为new_es_doc的子集
            consistence_cnt += 1
        else:
            # 统计不一致的情况
            diff_cols = [k for k in old_es_doc.keys() if old_es_doc.get(k) != new_es_doc.get(k)]
            user_id = old_es_doc.get('userid')
            logger.debug("新旧es doc不一致 userid:%s （lastLoginTime old:%s new:%s）差异字段:%s" % (user_id, old_es_doc.get('lastLoginTime'), new_es_doc.get('lastLoginTime'),",".join(diff_cols)))
            if "lastLoginTime" in diff_cols:
                logger.info("------lastLoginTime存在差异的userid:%s （lastLoginTime old:%s  new:%s）-----" % (user_id, old_es_doc.get('lastLoginTime'), new_es_doc.get('lastLoginTime')))
            # inconsistent_dict.setdefault(",".join(diff_cols), []).append(user_id)
            for diff_col in diff_cols:
                inconsistent_dict[diff_col] = 1 if inconsistent_dict.get(diff_col) is None else inconsistent_dict[diff_col] + 1

    logger.info("本批次对比总条数:%s 一致的条数:%s  一致率:%s%% 耗时:%.3f秒 不一致情况统计:%s"
                % (total_cnt, consistence_cnt, float(consistence_cnt)/total_cnt * 100, time.time() - st, str(inconsistent_dict)))
    return total_cnt, consistence_cnt, inconsistent_dict


def check_data(gte, lte, step_size=10000, limit=-1):
    query_summary = """
    {
      "query": {
        "range": {
          "updateTime": {
            "gte": "%s",
            "lte": "%s",
            "format": "yyyy-MM-dd HH:mm:ss.SSS"
          }
        }
      }
    }
    """ % (gte, lte)
    summary_json = query_es("_search", query_summary, OLD_ES_ADDR, OLD_ES_AUTH, OLD_ES_INDEX)
    total = summary_json.get('hits').get('total')
    if limit != -1:
        if limit < step_size:
            step_size = limit
        total = limit

    logger.info("check_data本次验证数据量TotalCnt: %s" % total)

    all_inconsistent = {}

    total_checked = 0
    total_consistence = 0

    result_cnt = -1
    old_scroll_id = ""
    new_scroll_id = ""
    fitst_query = """
            {
              "size": %s,
              "query": {
                "range": {
                  "updateTime": {
                    "gte": "%s",
                    "lte": "%s",
                    "format": "yyyy-MM-dd HH:mm:ss.SSS"
                  }
                }
              },
               "sort": {
                  "userid" : {
                      "order": "desc"
                   }
                }
            }
            """ % (step_size, gte, lte)
    while total_checked < total:
        if result_cnt == -1:
            # 首次运行 拿到scroll id
            old_data = query_es("_search?scroll=5m", fitst_query, OLD_ES_ADDR, OLD_ES_AUTH, OLD_ES_INDEX)
            new_data = query_es("_search?scroll=5m", fitst_query, NEW_ES_ADDR, NEW_ES_AUTH, NEW_ES_INDEX)
            old_scroll_id = old_data.get('_scroll_id')
            new_scroll_id = new_data.get('_scroll_id')
            checked_cnt, consist_cnt, inconsistent_dict = check_data_consistency(old_data, new_data)
            total_checked += checked_cnt
            total_consistence += consist_cnt
            result_cnt = total_checked

            all_inconsistent.update(inconsistent_dict)
        else:
            old_after_query = """
            {
                "scroll" : "5m",
                "scroll_id":"%s"
            }
            """ % old_scroll_id
            new_after_query = """
            {
                "scroll" : "5m",
                "scroll_id":"%s"
            }
            """ % new_scroll_id
            old_data = query_es("_search/scroll", old_after_query, OLD_ES_ADDR, OLD_ES_AUTH, "")
            new_data = query_es("_search/scroll", new_after_query, NEW_ES_ADDR, NEW_ES_AUTH, "")

            checked_cnt, consist_cnt, inconsistent_dict = check_data_consistency(old_data, new_data)
            if len(inconsistent_dict) != 0:
                for diff_col, cnt in inconsistent_dict.items():
                    all_inconsistent[diff_col] = cnt if all_inconsistent.get(diff_col) is None else all_inconsistent[diff_col] + cnt

            total_checked += checked_cnt
            total_consistence += consist_cnt

    logger.info("数据验证完成，时间范围%s ~ %s，总验证条数%s，一致率:%s%%" % (gte, lte, total_checked, float(total_consistence)/total_checked*100))
    if all_inconsistent != {}:
        logger.info("不一致的情况汇总：%s" % str(all_inconsistent))


if __name__ == '__main__':
    # check历史数据
    # check_data("2018-08-11 16:59:33.000", "2018-08-11 17:00:00.000")
    # check_data("2018-08-11 16:29:33.000", "2018-08-11 17:00:00.000")
    # check_data("2018-08-12 16:29:33.000", "2018-08-12 17:00:00.000")

    # check新数据
    # check_data("2022-06-05 00:00:00.000", "2022-06-05 00:10:00.000", 10, 80)
    # check_data("2022-06-05 00:00:00.000", "2022-06-06 06:02:00.000", 50, 10000)

    # check_data("2022-06-06 06:00:00.000", "2022-06-07 16:02:00.000", 100, 20000)
    check_data("2022-06-02 06:00:00.000", "2022-06-03 16:00:00.000", 50, 20000)
    check_data("2022-06-02 06:00:00.000", "2022-06-03 16:00:00.000", 50, 20000)
    check_data("2022-06-05 00:00:00.000", "2022-06-06 01:00:00.000", 1000, 2000)







