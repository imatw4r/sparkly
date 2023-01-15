from typing import Any

from pydantic import BaseSettings, PostgresDsn, SecretStr


class LoggerSettings(BaseSettings):
    LEVEL: str = "DEBUG"
    FORMAT: str = "%(log_color)s%(asctime)s.%(msecs)03d | " + "%(levelname)s | %(name)3s:%(lineno)d | %(message)s"

    def get_config(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored_verbose": {
                    "()": "colorlog.ColoredFormatter",
                    "format": self.FORMAT,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "colored_console": {
                    "formatter": "colored_verbose",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "level": self.LEVEL,
                },
            },
            "loggers": {
                "root": {"handlers": ["colored_console"], "level": self.LEVEL},
            },
        }

    class Config:
        use_enum_values = True
        fields = {
            "LEVEL": {"env": ["LOGGER_LEVEL"]},
            "FORMAT": {"env": ["LOGGER_FORMAT"]},
        }


class DatabaseSettings(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    NAME: str
    HOST: str
    PORT: str = "5432"

    ECHO_LOGS: bool = True
    ENABLE_PROFILER: bool = True

    def _get_uri(self, schema: str) -> SecretStr:
        uri = PostgresDsn.build(
            scheme=schema,
            user=self.USER,
            password=self.PASSWORD.get_secret_value(),
            path=f"/{self.NAME}",
            port=self.PORT,
            host=self.HOST,
        )
        return SecretStr(value=uri)

    def get_async_uri(self) -> SecretStr:
        return self._get_uri(schema="postgresql+asyncpg")

    def get_sync_uri(self) -> SecretStr:
        return self._get_uri(schema="postgresql+psycopg2")

    class Config:
        env_file = ".env"
        case_sensitive = True
        fields = {
            "USER": {"env": ["POSTGRES_USER"]},
            "PASSWORD": {"env": ["POSTGRES_PASSWORD"]},
            "NAME": {"env": ["POSTGRES_DB_NAME"]},
            "HOST": {"env": ["POSTGRES_HOST"]},
            "PORT": {"env": ["POSTGRES_PORT"]},
            "ECHO_LOGS": {"env": ["DB_ECHO_LOGS"]},
        }


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    logger: LoggerSettings = LoggerSettings()

    class Config:
        env_file = ".env"
        case_sensitive = True
