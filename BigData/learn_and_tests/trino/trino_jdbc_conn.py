from sqlalchemy import create_engine, text
from trino.auth import BasicAuthentication

# pip install --user trino sqlalchemy=1.3.24 (2.0.21)

engine = create_engine("trino://username@trino_host:7778/hive/default",
    connect_args={
        # "auth": CertificateAuthentication("cert.pem", "trino.key"),  # 可忽略
        "auth": BasicAuthentication("username", "pwd"),
        "http_scheme": "https",
        "verify": False  # 忽略SSL证书验证
    }
)

connection = engine.connect()
rows = connection.execute(text("SELECT * FROM dual")).fetchall()
print(rows)
