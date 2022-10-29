import pydantic as pyd

class QbtAccessConfig(pyd.BaseModel):
    host: str
    port: int
    username: str
    password: str


class Config(pyd.BaseModel):
    qbt_access: QbtAccessConfig
    expire_default: int



def produce_default_config() -> Config:
    return Config(
        qbt_access=QbtAccessConfig(
            host='localhost',
            port=8080,
            username='user',
            password='pass'
        ),
        expire_default=30
    )