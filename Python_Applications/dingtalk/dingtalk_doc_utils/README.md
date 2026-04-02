# dingtalk_doc_utils 线上部署说明

`dingtalk_doc_utils` 是钉钉文档读取的通用工具包，核心类为 `DingTalkDocReader`。

## 目录结构

- `reader.py`：工具包核心实现（含超时、重试、结构化日志）
- `__init__.py`：对外导出 `DingTalkDocReader` 与 `read_dingtalk_sheet`

## 一、线上部署方式

推荐两种方式：

1. **随业务仓库部署（当前方式）**
   - 直接在业务代码里引用：
     - `from dingtalk_doc_utils import DingTalkDocReader`
2. **独立内部包部署（推荐长期方案）**
   - 抽成独立仓库并发布到私有 PyPI
   - 业务服务通过 `pip install dingtalk_doc_utils-0.1.0-py3-none-any.whl` 安装

### 当前目录的 wheel 打包方式（你要求的方案A）

以下命令都在 `dingtalk_doc_utils` 目录执行，且 wheel 产物直接输出到当前目录（不会输出到上层目录）：
产出dingtalk_doc_utils-0.1.0-py3-none-any.whl安装包
```bash
cd /home/shmily/Projects/MyProjects/PythonProjects/Shmily-py/Python_Applications/dingtalk/dingtalk_doc_utils
/usr/lib/miniconda3/envs/py38_default/bin/python -m pip install -U pip build
/usr/lib/miniconda3/envs/py38_default/bin/python -m build --wheel --outdir .
```

安装到你的线上环境：

```bash
/usr/lib/miniconda3/envs/py38_default/bin/python -m pip install ./dingtalk_doc_utils-0.1.0-py3-none-any.whl
```

验证导入：

```bash
/usr/lib/miniconda3/envs/py38_default/bin/python -c "from dingtalk_doc_utils import DingTalkDocReader; print('import ok')"
```

## 二、运行环境要求

- Python >= 3.7
- 依赖：
  - `requests`
  - `pandas`

## 三、环境变量配置（生产必须）

在服务启动环境中配置：

- `DINGTALK_APP_KEY`：钉钉应用 AppKey
- `DINGTALK_APP_SECRET`：钉钉应用 AppSecret
- `DINGTALK_OPERATOR_ID`：操作者 unionId（推荐）
- `DINGTALK_OPERATOR_MOBILE`：操作者手机号（可选，`OPERATOR_ID` 为空时自动换取 unionId）
- `DINGTALK_WORKBOOK_URL`：钉钉文档 URL
- `DINGTALK_SHEET_ID`：工作表 ID（可选，不填可用 `sheetId` 自动取第一张）
- `DINGTALK_RANGE`：读取范围（可选）
- `DINGTALK_HEADER_ROW`：表头行号（默认 1）

示例（Linux）：

```bash
export DINGTALK_APP_KEY="xxx"
export DINGTALK_APP_SECRET="xxx"
export DINGTALK_OPERATOR_ID="xxx"
export DINGTALK_WORKBOOK_URL="https://alidocs.dingtalk.com/i/nodes/xxxx"
```

## 四、业务代码接入示例

```python
import os
from Python_Applications.dingtalk.dingtalk_doc_utils import DingTalkDocReader

reader = DingTalkDocReader(
    app_key=os.getenv("DINGTALK_APP_KEY", ""),
    app_secret=os.getenv("DINGTALK_APP_SECRET", ""),
    operator_id=os.getenv("DINGTALK_OPERATOR_ID", ""),
    operator_mobile=os.getenv("DINGTALK_OPERATOR_MOBILE", ""),
    timeout=15,
    max_retries=3,
    backoff_factor=0.5,
)

df = reader.read_sheet_to_dataframe(
    workbook_url=os.getenv("DINGTALK_WORKBOOK_URL", ""),
    sheet_id=os.getenv("DINGTALK_SHEET_ID", "sheetId"),
    range_=os.getenv("DINGTALK_RANGE", "") or None,
    header_row=int(os.getenv("DINGTALK_HEADER_ROW", "1")),
)
```

## 五、线上稳定性建议

1. **密钥管理**
   - 使用 K8s Secret / CI Secret 注入环境变量
   - 不要把 `APP_KEY/APP_SECRET` 写死在代码或配置文件
2. **日志管理**
   - 当前已输出结构化日志
   - 日志中不打印密钥与 token
3. **重试与超时**
   - 默认超时 15 秒、重试 3 次
   - 可按业务 SLA 调整
4. **权限检查**
   - 应用需开通 `Document.Workbook.Read`
   - `operatorId` 对应用户必须具备文档访问权限

## 六、常见故障排查

1. `403 Forbidden`
   - 检查应用权限是否开通
   - 检查文档是否共享给 `operatorId` 对应用户
2. `400 ... at most 30000 cells`
   - 工具已支持自动分块读取；如手动传了超大 `RANGE`，请缩小范围
3. `未读取到 DINGTALK_APP_KEY 或 DINGTALK_APP_SECRET`
   - 环境变量未注入或变量名错误
4. `operator_id 与 operator_mobile 不能同时为空`
   - 至少配置其中一个

