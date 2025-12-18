from pydantic import BaseModel, ConfigDict


# Region schemas
class RegionBase(BaseModel):
    name: str


class RegionCreate(RegionBase):
    pass


class RegionResponse(RegionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# City schemas
class CityBase(BaseModel):
    name: str
    region_id: int


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Region with cities
class RegionWithCities(RegionResponse):
    cities: list[CityResponse] = []

    model_config = ConfigDict(from_attributes=True)
