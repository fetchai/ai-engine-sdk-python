from typing import Dict, List, Union
from pydantic import BaseModel


class CustomModel(BaseModel):
    id: str
    name: str


model_names: Dict[str, str] = {
    "thoughtful-01": "Thoughtful",
    "talkative-01": "Talkative",
    "talkative-02": "Talkative 2",
    "talkative-03": "Talkative 3",
    "creative-01": "Creative",
    "creative-02": "Creative 2",
    "creative-03": "Creative 3",
    "creative-04": "Creative 4",
    "gemini-pro": "Gemini Pro",
    "next-gen": "Next Generation",
    "ml-recommender-01": "ML Recommender",
}

KnownModelId = str  # Alias for type hinting

DefaultModelIds: List[KnownModelId] = [
    "thoughtful-01",
    "talkative-01",
    "creative-01",
    "gemini-pro",
    "next-gen",
    "ml-recommender-01",
]

DefaultModelId: KnownModelId = "talkative-01"


def get_model_id(model: Union[KnownModelId, CustomModel]) -> str:
    if isinstance(model, str):
        return model
    return model.id


def get_model_name(model: Union[KnownModelId, CustomModel]) -> str:
    if isinstance(model, str):
        return model_names.get(model, "Unknown Model")
    return model.name
