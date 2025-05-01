from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = True

    discord_token: str = ""
    discord_prefix: str = "gg2"
    discord_test_guild: int | None = None

    gg2_host: str = "0.0.0.0"
    gg2_port: int = 51061
    gg2_timeout: float = 3.0

    active_contracts_per_user: int = 3

    webapp_host: str = "0.0.0.0"
    webapp_port: int = 80
    webapp_ssl_certfile: str = ""
    webapp_ssl_keyfile: str = ""
    webapp_workers: int = 1

    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db_name: str = "contracts"

    sqlite_file_name: str = "database.db"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def db_uri(self) -> str:
        if self.postgres_host:
            return MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db_name,
            ).unicode_string()
        else:
            return f"sqlite:///{self.sqlite_file_name}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
