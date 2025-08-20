from pydantic import BaseModel, ConfigDict
from pydantic_mongo import AbstractRepository, PydanticObjectId
from pymongo import MongoClient
from typing import Optional


# Basic class - comes in as request data as well as used in DB
class Opportunity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    opportunity_id: str
    url: str
    title: str
    industry: str
    application_text: Optional[str]
    status: str

# Used for DB interaction
class OpportunityDataClass(Opportunity):
   # PydanticObjectId is an alias to Annotated[ObjectId, ObjectIdAnnotation]
   id: Optional[PydanticObjectId] = None


# Create a repository
class OpportunityRepository(AbstractRepository[OpportunityDataClass]):
   class Meta:
      collection_name = 'opportunities'

# Connect to database
client = MongoClient("mongodb://localhost:27017", username = "root", password = "password")
database = client["example"]
opportunity_repo = OpportunityRepository(database)

