from typing import Union
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


# To support new models add them to the model field!
class Embeddings:
    def __init__(self, embeddings: list[list[float]], model: Union[OpenAIEmbeddings, OllamaEmbeddings]):
        self._embeddings = embeddings
        self._model = model

    @property
    def embeddings(self) -> list[list[float]]:
        """The list of embeddings generated by the model."""
        return self._embeddings

    @property
    def embeddings_model(self) -> Union[OpenAIEmbeddings, OllamaEmbeddings]:
        """Model used to generate embeddings."""
        return self._model
