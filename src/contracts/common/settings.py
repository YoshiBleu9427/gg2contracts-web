from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gg2_host: str = "0.0.0.0"
    gg2_port: int = 4646
    gg2_timeout: float = 3.0

    active_contracts_per_user: int = 3

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
