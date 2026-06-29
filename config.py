from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    database_name: str
    database_user: str
    database_host: str
    database_port: int
    groq_api_key: str
    hf_token: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_token_expiry: int
    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()