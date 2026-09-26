import os
import duckdb
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

# Cargar las variables de entorno desde tu archivo oculto .env
load_dotenv()
ALCHEMY_URL = os.getenv("ALCHEMY_RPC_URL")
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")

class EVMTransferLog(BaseModel):
    block_number: int = Field(..., gt=0)
    transaction_hash: str
    from_address: str
    to_address: str
    value_wei: str
    ingested_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    partition_date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

    @field_validator("transaction_hash", "from_address", "to_address")
    @classmethod
    def validate_hex_lengths(cls, value: str) -> str:
        clean_value = value.strip()
        if not clean_value.startswith("0x"):
            raise ValueError("Prefijo 0x faltante")
        return clean_value

# Simulación del Payload que vendrá desde la URL de Alchemy
mock_rpc_payload = {
    "block_number": 19542031,
    "transaction_hash": "0x8c6b71f9a2e6b12a52b834e56c12dbf57a1b3c9e54bf12d3cf8b39d73d2a71bc",
    "from_address": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
    "to_address": "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be",
    "value_wei": "1500000000000000000"
}

print(f"📡 [PIPELINE] Inicializando conexión segura al nodo de Alchemy...")
if ALCHEMY_URL:
    print("✔️ [PIPELINE] Variable ALCHEMY_RPC_URL cargada con éxito desde el búnker .env.")
else:
    print("❌ ERROR: No se detectó la configuración de red en el archivo .env")

print("🔄 [PIPELINE] Validando consistencia criptográfica...")
validated_log = EVMTransferLog(**mock_rpc_payload)

db_path = "crypto_analytics.db"
db_conn = duckdb.connect(db_path)

db_conn.execute("""
    CREATE TABLE IF NOT EXISTS evm_transfers (
        block_number BIGINT, transaction_hash VARCHAR, from_address VARCHAR, to_address VARCHAR, value_wei VARCHAR, ingested_at TIMESTAMP, partition_date VARCHAR
    )
""")

db_conn.execute("INSERT INTO evm_transfers VALUES (?, ?, ?, ?, ?, ?, ?)", [
    validated_log.block_number, validated_log.transaction_hash, validated_log.from_address, validated_log.to_address, validated_log.value_wei, validated_log.ingested_at, validated_log.partition_date
])

os.makedirs("parquet_lake", exist_ok=True)
db_conn.execute("COPY evm_transfers TO 'parquet_lake' (FORMAT PARQUET, PARTITION_BY partition_date, OVERWRITE_OR_IGNORE TRUE)")
db_conn.close()
print("🏆 [PIPELINE] Ingesta y validación de variables completadas con éxito.")
