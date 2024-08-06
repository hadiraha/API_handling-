#Pydantic models
from pydantic import BaseModel, field_validator, constr, ConfigDict, Field

class ProfileBase(BaseModel): # We constrain values to make them readable for pydantic and API
    username: constr(strip_whitespace=True) # type: ignore
    name: constr(strip_whitespace=True) # type: ignore
    pic_s: constr(strip_whitespace=True) # type: ignore
    follower_cnt: constr(strip_whitespace=True) # type: ignore
    follow_cnt: constr(strip_whitespace=True) # type: ignore
    url: constr(strip_whitespace=True) # type: ignore
    video_cnt: constr(strip_whitespace=True) # type: ignore
    video_visit: constr(strip_whitespace=True) # type: ignore
    description: constr(strip_whitespace=True) # type: ignore
    follower_cnt_num: constr(strip_whitespace=True) # type: ignore

    @field_validator('*', mode='before') # We should ensure that validation is done for avoid mismatching problmes
    def ensure_string(cls, v):
        if v is None:
            return ""
        return str(v)

    model_config = ConfigDict(from_attributes=True)

class Profile(ProfileBase):
    id: int = Field(..., alias="id")

    # @field_validator('*', mode='before')
    # def ensure_string(cls, v):
    #     if v is None:
    #         return ""
    #     return str(v)

    model_config = ConfigDict(from_attributes=True)