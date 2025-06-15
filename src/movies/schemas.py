from pydantic import BaseModel, condecimal, ConfigDict
from typing import List, Optional
from decimal import Decimal

class GenreSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class StarSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class DirectorSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class CertificationSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class MovieBaseSchema(BaseModel):
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: condecimal(max_digits=10, decimal_places=2)
    certification_id: int
    genre_ids: List[int]
    director_ids: List[int]
    star_ids: List[int]

class MovieCreateSchema(MovieBaseSchema):
    pass

class MovieSchema(MovieBaseSchema):
    id: int
    uuid: str
    genres: List[GenreSchema]
    directors: List[DirectorSchema]
    stars: List[StarSchema]
    certification: CertificationSchema

    model_config = ConfigDict(from_attributes=True)
