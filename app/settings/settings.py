from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_TEST_HOST: str = '127.0.0.1'
    POSTGRES_TEST_PORT: int = 5432
    POSTGRES_TEST_USER: str = 'test'
    POSTGRES_TEST_PASSWORD: str = 'test'
    POSTGRES_TEST_DB: str = 'test_shop'

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def postgres_url(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    @property
    def test_postgres_url(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_TEST_USER}:{self.POSTGRES_TEST_PASSWORD}'
                f'@{self.POSTGRES_TEST_HOST}:{self.POSTGRES_TEST_PORT}/{self.POSTGRES_TEST_DB}')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
