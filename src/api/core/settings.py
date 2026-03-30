"""Configurações globais da aplicação utilizando Pydantic Settings."""

from typing import Set
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Classe de configuração que carrega variáveis de ambiente."""

    database_url: str = Field(..., alias="DATABASE_URL")
    db_target: str | None = Field(None, alias="DB_TARGET")
    env: str = Field("dev", alias="ENV")

    default_page_size: int = 100
    max_page_size: int = 1000

    allowed_variables: Set[str] = {
        "wind_speed",
        "power",
        "ambient_temperature",
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    def get_page_size(self, requested: int | None) -> int:
        """
        Calcula o tamanho da página com base no valor solicitado e nos limites configurados.

        Args:
            requested (int | None): O tamanho da página solicitado pelo usuário.

        Returns:
            int: O tamanho da página final, respeitando o máximo permitido.
        """
        if requested is None:
            return self.default_page_size
        return min(requested, self.max_page_size)


settings = Settings()
