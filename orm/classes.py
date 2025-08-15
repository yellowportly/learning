from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId
from pymongo import MongoClient
from typing import Optional, List

# Define your models
class Opportunity(BaseModel):
   # PydanticObjectId is an alias to Annotated[ObjectId, ObjectIdAnnotation]
   id: Optional[PydanticObjectId] = None
   opportunity_id: str
   url: str
   title: str
   industry: str
   application_text: str
   status: str


# Create a repository
class OpportunityRepository(AbstractRepository[Opportunity]):
   class Meta:
      collection_name = 'opportunities'

# Connect to database
client = MongoClient("mongodb://localhost:27017", username = "root", password = "password")
database = client["example"]
repo = OpportunityRepository(database)

