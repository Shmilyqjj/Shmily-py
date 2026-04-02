"""
钉钉文档（在线Excel）数据读取工具
可作为独立 util 包被业务脚本引入。
"""

import json
import logging
import re
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class DingTalkDocReader:
    """钉钉文档读取器（支持超时、重试、结构化日志）"""

    BASE_URL = "https://api.dingtalk.com"
    OAPI_URL = "https://oapi.dingtalk.com"

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        operator_id: str = "",
        operator_mobile: str = "",
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.app_key = app_key
        self.app_secret = app_secret
        self.operator_id = operator_id
        self.operator_mobile = operator_mobile
        self.timeout = timeout
        self.access_token: Optional[str] = None

        self._validate_init_params()
        self.session = self._build_session(max_retries=max_retries, backoff_factor=backoff_factor)

        self._log("info", "reader_initialized", has_operator_id=bool(self.operator_id), has_operator_mobile=bool(self.operator_mobile))

    def _validate_init_params(self) -> None:
        if not self.app_key or not self.app_secret:
            raise ValueError(
                "未读取到 DINGTALK_APP_KEY 或 DINGTALK_APP_SECRET。"
                "请在系统环境变量中配置后重试。"
            )
        if not self.operator_id and not self.operator_mobile:
            raise ValueError(
                "请配置 operator_id 或 operator_mobile。"
                "operator_id 优先；若为空可通过 operator_mobile 自动换取 unionid。"
            )

    def _build_session(self, max_retries: int, backoff_factor: float) -> requests.Session:
        session = requests.Session()
        retry_kwargs = dict(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            raise_on_status=False,
        )
        try:
            retry = Retry(allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE"]), **retry_kwargs)
        except TypeError:
            # 兼容低版本 urllib3
            retry = Retry(method_whitelist=frozenset(["GET", "POST", "PUT", "DELETE"]), **retry_kwargs)

        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _log(self, level: str, event: str, **kwargs: Any) -> None:
        payload = {"event": event, **kwargs}
        message = json.dumps(payload, ensure_ascii=False, default=str)
        getattr(logger, level, logger.info)(message)

    def _request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        action: str = "",
    ) -> requests.Response:
        start = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )
            cost_ms = int((time.time() - start) * 1000)
            self._log(
                "info",
                "http_request_done",
                action=action,
                method=method,
                url=url,
                status_code=response.status_code,
                cost_ms=cost_ms,
            )
            return response
        except Exception as exc:
            cost_ms = int((time.time() - start) * 1000)
            self._log(
                "error",
                "http_request_error",
                action=action,
                method=method,
                url=url,
                cost_ms=cost_ms,
                error=str(exc),
            )
            raise

    def get_access_token(self) -> str:
        url = f"{self.OAPI_URL}/gettoken"
        params = {"appkey": self.app_key, "appsecret": self.app_secret}
        response = self._request("GET", url, params=params, action="get_access_token")
        result = response.json()
        if result.get("errcode") != 0:
            raise Exception(f"获取access_token失败: {result.get('errmsg')}")
        self.access_token = result["access_token"]
        self._log("info", "access_token_refreshed")
        return self.access_token

    def get_userid_by_mobile(self, mobile: str) -> str:
        if not mobile:
            raise ValueError("mobile 不能为空")
        if not self.access_token:
            self.get_access_token()
        url = f"{self.OAPI_URL}/topapi/v2/user/getbymobile"
        response = self._request(
            "POST",
            url,
            params={"access_token": self.access_token},
            json_body={"mobile": mobile},
            action="get_userid_by_mobile",
        )
        result = response.json()
        if result.get("errcode") != 0:
            raise Exception(f"通过手机号获取userid失败: {result}")
        userid = result.get("result", {}).get("userid")
        if not userid:
            raise Exception(f"通过手机号获取userid失败，响应缺少userid: {result}")
        return userid

    def get_unionid_by_userid(self, userid: str) -> str:
        if not userid:
            raise ValueError("userid 不能为空")
        if not self.access_token:
            self.get_access_token()
        url = f"{self.OAPI_URL}/topapi/v2/user/get"
        response = self._request(
            "POST",
            url,
            params={"access_token": self.access_token},
            json_body={"userid": userid},
            action="get_unionid_by_userid",
        )
        result = response.json()
        if result.get("errcode") != 0:
            raise Exception(f"通过userid获取unionid失败: {result}")
        unionid = result.get("result", {}).get("unionid")
        if not unionid:
            raise Exception(f"通过userid获取unionid失败，响应缺少unionid: {result}")
        return unionid

    def resolve_operator_id(self, operator_id: Optional[str] = None, operator_mobile: Optional[str] = None) -> str:
        actual_operator_id = self.operator_id if operator_id is None else operator_id
        actual_operator_mobile = self.operator_mobile if operator_mobile is None else operator_mobile
        if actual_operator_id:
            return actual_operator_id
        if actual_operator_mobile:
            userid = self.get_userid_by_mobile(actual_operator_mobile)
            return self.get_unionid_by_userid(userid)
        raise ValueError("operator_id 与 operator_mobile 不能同时为空")

    @staticmethod
    def _resolve_workbook_id(workbook_url: str) -> str:
        if not workbook_url:
            raise ValueError("workbook_url 不能为空")
        value = workbook_url.strip()
        if value.startswith("http://") or value.startswith("https://"):
            parsed = urlparse(value)
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 3 and parts[0] == "i" and parts[1] == "nodes" and parts[2]:
                return parts[2]
            raise ValueError(f"无法从URL中解析workbook_id: {value}")
        raise ValueError("workbook_url 必须为钉钉文档URL，不再支持直接传 workbook_id")

    def _get_headers(self) -> Dict[str, str]:
        if not self.access_token:
            self.get_access_token()
        return {"x-acs-dingtalk-access-token": self.access_token, "Content-Type": "application/json"}

    @staticmethod
    def _ensure_success(response: requests.Response, action: str) -> Dict[str, Any]:
        try:
            result = response.json()
        except ValueError:
            result = {"raw": response.text}
        if response.status_code >= 400:
            raise Exception(f"{action}失败: HTTP {response.status_code}, 响应: {result}")
        if isinstance(result, dict) and "code" in result and result["code"] != "Success":
            raise Exception(f"{action}失败: {result}")
        if isinstance(result, dict) and result.get("success") is False:
            raise Exception(f"{action}失败: {result}")
        return result

    def get_sheet_list(self, workbook_url: str, operator_id: Optional[str] = None) -> Dict[str, Any]:
        workbook_id = self._resolve_workbook_id(workbook_url)
        url = f"{self.BASE_URL}/v1.0/doc/workbooks/{workbook_id}/sheets"
        params = {"operatorId": self.resolve_operator_id(operator_id=operator_id)}
        response = self._request("GET", url, headers=self._get_headers(), params=params, action="get_sheet_list")
        return self._ensure_success(response, "获取工作表列表")

    def get_sheet_properties(self, workbook_url: str, sheet_id: str, operator_id: Optional[str] = None) -> Dict[str, Any]:
        workbook_id = self._resolve_workbook_id(workbook_url)
        url = f"{self.BASE_URL}/v1.0/doc/workbooks/{workbook_id}/sheets/{sheet_id}"
        params = {"operatorId": self.resolve_operator_id(operator_id=operator_id)}
        response = self._request("GET", url, headers=self._get_headers(), params=params, action="get_sheet_properties")
        return self._ensure_success(response, "获取工作表属性")

    def get_sheet_data(
        self,
        workbook_url: str,
        sheet_id: str,
        range_: Optional[str] = None,
        operator_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        workbook_id = self._resolve_workbook_id(workbook_url)
        range_address = range_ or "A1:AD1000"
        url = f"{self.BASE_URL}/v1.0/doc/workbooks/{workbook_id}/sheets/{sheet_id}/ranges/{range_address}"
        params = {"operatorId": self.resolve_operator_id(operator_id=operator_id)}
        response = self._request("GET", url, headers=self._get_headers(), params=params, action="get_sheet_data")
        return self._ensure_success(response, "读取工作表数据")

    @staticmethod
    def _col_index_to_letters(col_index: int) -> str:
        if col_index <= 0:
            raise ValueError("col_index 必须大于0")
        letters = []
        n = col_index
        while n > 0:
            n, rem = divmod(n - 1, 26)
            letters.append(chr(ord("A") + rem))
        return "".join(reversed(letters))

    @staticmethod
    def _extract_column_count(sheet_properties: Dict[str, Any]) -> Optional[int]:
        candidate_keys = {"columnCount", "colCount", "column_count", "cols", "columnNum"}
        stack = [sheet_properties]
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                for key, value in current.items():
                    if key in candidate_keys and isinstance(value, int) and value > 0:
                        return value
                    if isinstance(value, (dict, list)):
                        stack.append(value)
            elif isinstance(current, list):
                for item in current:
                    if isinstance(item, (dict, list)):
                        stack.append(item)
        return None

    def _read_sheet_data_in_chunks(
        self,
        workbook_url: str,
        sheet_id: str,
        operator_id: str,
        column_count: int,
        max_cells_per_request: int = 30000,
        max_chunks: int = 200,
    ) -> Dict[str, Any]:
        workbook_id = self._resolve_workbook_id(workbook_url)
        col_letters = self._col_index_to_letters(column_count)
        rows_per_chunk = max(1, max_cells_per_request // column_count)
        all_rows: List[List[Any]] = []
        start_row = 1
        empty_chunk_count = 0

        for _ in range(max_chunks):
            end_row = start_row + rows_per_chunk - 1
            range_address = f"A{start_row}:{col_letters}{end_row}"
            url = f"{self.BASE_URL}/v1.0/doc/workbooks/{workbook_id}/sheets/{sheet_id}/ranges/{range_address}"
            params = {"operatorId": operator_id}
            response = self._request("GET", url, headers=self._get_headers(), params=params, action="get_sheet_data_chunk")
            chunk_data = self._ensure_success(response, "读取工作表数据")
            grid = self._extract_grid(chunk_data)
            if not grid:
                empty_chunk_count += 1
            else:
                while grid and all((cell == "" or cell is None) for cell in grid[-1]):
                    grid.pop()
                if grid:
                    all_rows.extend(grid)
                    empty_chunk_count = 0
                else:
                    empty_chunk_count += 1
            if empty_chunk_count >= 2:
                break
            start_row = end_row + 1
        return {"values": all_rows}

    @staticmethod
    def _parse_cell_ref(cell_ref: str) -> Optional[tuple]:
        match = re.match(r"^([A-Z]+)(\d+)$", cell_ref.upper())
        if not match:
            return None
        col_letters, row_str = match.groups()
        row = int(row_str)
        col = 0
        for char in col_letters:
            col = col * 26 + (ord(char) - ord("A") + 1)
        return row, col

    def _extract_grid(self, data: Dict[str, Any]) -> List[List[Any]]:
        values = data.get("values")
        if isinstance(values, list) and values and isinstance(values[0], list):
            return values
        nested = data.get("data")
        if isinstance(nested, dict):
            nested_values = nested.get("values")
            if isinstance(nested_values, list) and nested_values and isinstance(nested_values[0], list):
                return nested_values
        cells = data.get("cells")
        if isinstance(cells, list):
            if not cells:
                return []
            max_row = max(int(c.get("row", 0)) for c in cells)
            max_col = max(int(c.get("col", 0)) for c in cells)
            grid = [[""] * max_col for _ in range(max_row)]
            for cell in cells:
                row = int(cell.get("row", 0)) - 1
                col = int(cell.get("col", 0)) - 1
                if row >= 0 and col >= 0:
                    grid[row][col] = cell.get("value", "")
            return grid
        if isinstance(cells, dict):
            parsed_cells = []
            for ref, payload in cells.items():
                position = self._parse_cell_ref(ref)
                if not position:
                    continue
                row, col = position
                value = payload
                if isinstance(payload, dict):
                    value = payload.get("value") if payload.get("value") is not None else payload.get("displayValue")
                parsed_cells.append({"row": row, "col": col, "value": value if value is not None else ""})
            if not parsed_cells:
                return []
            max_row = max(cell["row"] for cell in parsed_cells)
            max_col = max(cell["col"] for cell in parsed_cells)
            grid = [[""] * max_col for _ in range(max_row)]
            for cell in parsed_cells:
                grid[cell["row"] - 1][cell["col"] - 1] = cell["value"]
            return grid
        return []

    @staticmethod
    def _is_empty_cell(value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ""
        return False

    def _trim_grid(self, grid: List[List[Any]]) -> List[List[Any]]:
        if not grid:
            return []
        max_len = max(len(row) for row in grid)
        normalized = [row + [""] * (max_len - len(row)) for row in grid]
        while normalized and all(self._is_empty_cell(cell) for cell in normalized[-1]):
            normalized.pop()
        if not normalized:
            return []
        last_used_col = -1
        for row in normalized:
            for col_idx, cell in enumerate(row):
                if not self._is_empty_cell(cell):
                    last_used_col = max(last_used_col, col_idx)
        if last_used_col < 0:
            return []
        return [row[: last_used_col + 1] for row in normalized]

    def sheet_data_to_dataframe(self, data: Dict[str, Any], header_row: int = 1) -> pd.DataFrame:
        grid = self._trim_grid(self._extract_grid(data))
        if not grid:
            return pd.DataFrame()
        if header_row > 0 and len(grid) >= header_row:
            headers = grid[header_row - 1]
            data_rows = grid[header_row:]
            return pd.DataFrame(data_rows, columns=headers)
        return pd.DataFrame(grid)

    def read_sheet_to_dataframe(
        self,
        workbook_url: str,
        sheet_id: str = "sheetId",
        range_: Optional[str] = None,
        header_row: int = 1,
    ) -> pd.DataFrame:
        workbook_id = self._resolve_workbook_id(workbook_url)
        actual_operator_id = self.resolve_operator_id()
        actual_sheet_id = sheet_id
        if not actual_sheet_id or actual_sheet_id == "sheetId":
            sheet_list_result = self.get_sheet_list(workbook_url, operator_id=actual_operator_id)
            sheets = sheet_list_result.get("sheets", [])
            if not sheets:
                raise Exception("未找到可读取的工作表，请检查文档权限或sheet_id是否正确")
            first_sheet = sheets[0]
            actual_sheet_id = first_sheet.get("sheetId") or first_sheet.get("id") or first_sheet.get("title")
            if not actual_sheet_id:
                raise Exception(f"无法从工作表列表中解析sheet_id: {sheet_list_result}")

        if range_:
            data = self.get_sheet_data(workbook_url, actual_sheet_id, range_, operator_id=actual_operator_id)
        else:
            inferred_col_count = 26
            try:
                sheet_properties = self.get_sheet_properties(workbook_url, actual_sheet_id, operator_id=actual_operator_id)
                parsed_col_count = self._extract_column_count(sheet_properties)
                if parsed_col_count:
                    inferred_col_count = max(1, min(parsed_col_count, 702))
            except Exception:
                inferred_col_count = 26
            data = self._read_sheet_data_in_chunks(
                workbook_url=workbook_url,
                sheet_id=actual_sheet_id,
                operator_id=actual_operator_id,
                column_count=inferred_col_count,
            )
        return self.sheet_data_to_dataframe(data, header_row)


def read_dingtalk_sheet(
    app_key: str,
    app_secret: str,
    workbook_url: str,
    sheet_id: str = "sheetId",
    range_: Optional[str] = None,
    header_row: int = 1,
    operator_id: str = "",
    operator_mobile: str = "",
) -> pd.DataFrame:
    reader = DingTalkDocReader(
        app_key=app_key,
        app_secret=app_secret,
        operator_id=operator_id,
        operator_mobile=operator_mobile,
    )
    return reader.read_sheet_to_dataframe(workbook_url, sheet_id, range_, header_row)
