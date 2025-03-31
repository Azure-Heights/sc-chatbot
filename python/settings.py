"""Application-wide settings."""


from pydantic import Field
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


class AppSettings(BaseSettings):

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"

    anonymized_telemetry: bool = Field(
        False,
        description="Whether Chroma collects anonymous usage data."
    )

    proceedings_path: str = Field(
        "./sc.pdf",
        description="Location of the conference proceedings relative to the run directory."
    )

    langsmith_api_key: str = Field("", description="API key for LangSmith's monitoring service.")

    api_url: str = Field(alias="openai_base_url", description="LLM inference API endpoint.")
    api_key: str = Field(alias="openai_api_key",  description="API key for the inference endpoint.")

    model: str = Field(
        # "neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8",
        "meta-llama/Llama-3.3-70B-Instruct",
        description="The model used for inference."
    )

    embedding_dim: int = Field(384, description="The dimension of the embedding model output.")
    embedding_model: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2",
        description="The model used for embeddings."
    )

app_settings = AppSettings()
load_dotenv(app_settings.Config.env_file)


ABSTRACT_JSON_PATH = "./abstracts.json"


if __name__ == "__main__":
    print(app_settings.model_dump())

