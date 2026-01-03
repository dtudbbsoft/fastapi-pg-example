from typing import Optional
from pydantic import BaseModel, ConfigDict
from src.utils.constants import OnboardingStatusEnum

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    externalId: Optional[str]
    name: Optional[str]
    email: Optional[str]
    onboardingStatus: Optional[OnboardingStatusEnum]

class UserPayload(BaseModel):
    externalId: Optional[str]
    name: Optional[str]
    email: Optional[str]

