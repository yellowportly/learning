from bson import ObjectId
from pydantic import TypeAdapter
from pymongo.results import UpdateResult

from orm.classes import Opportunity, opportunity_repo
import json

def upsert_opportunity(msg: str):
    json_msg = json.loads(msg)

    found_opportunity = find_by_opportunity_id(json_msg['opportunity_id'])

    if found_opportunity is None:
        # validate message is ok then create new object
        if validate_input(json_msg):
            found_opportunity = TypeAdapter(Opportunity).validate_json(msg)
        else:
            print("Could not insert data")
            return -1
    else:
        # just update the values that were provided for keys
        found_opportunity.__dict__.update(json_msg)

    upserted_opportunity = do_actual_upsert(found_opportunity)

    # Check if updated or added
    if isinstance(upserted_opportunity, UpdateResult):
        return "Updated", found_opportunity.id
    else:
        return "Insrted", upserted_opportunity.inserted_id

def do_actual_upsert(found_opportunity: Opportunity):
    ret = opportunity_repo.save(found_opportunity)
    return ret

def do_update_from_object(request_opportunity: Opportunity):
    updated = opportunity_repo.save(request_opportunity)
    newly_found_opportunity = find_by_opportunity_id(opportunity_id=request_opportunity.opportunity_id)
    return newly_found_opportunity

async def find_by_opportunity_id_async(opportunity_id: str):
    return find_by_opportunity_id(opportunity_id)

def find_all_opportunities():
    #opportunities = opportunity_repo.find_by({"opportunity_id": {"$gte": "1"}})
    opportunities = opportunity_repo.get_collection().find()
    return opportunities

def find_by_opportunity_id(opportunity_id: str):
    ret = opportunity_repo.find_one_by({"opportunity_id": opportunity_id})
    print(f"Looking for: {opportunity_id} Found in method: {ret}")
    return ret

# Might be able to replace this with
def validate_input(json_msg: str):
    set_of_keys_in_msg = set(json_msg.keys())
    set_of_keys_in_model = set(Opportunity.model_fields.keys())

    # Remove id to allow comparison
    set_of_keys_in_model.remove("id")

    if set_of_keys_in_msg != set_of_keys_in_model:
        print(f"Keys don't match ! You gave me {set_of_keys_in_msg} and I wanted {set_of_keys_in_model}")
        return False

    return True