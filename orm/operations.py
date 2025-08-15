from pydantic import TypeAdapter
from pymongo.results import UpdateResult

from orm.classes import Opportunity, repo
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

    ret = repo.save(found_opportunity)

    # Check if updated or added
    if isinstance(ret, UpdateResult):
        return found_opportunity.id
    else:
        return ret.inserted_id

def find_by_opportunity_id(opportunity_id: str):
    ret = repo.find_one_by({"opportunity_id": opportunity_id})
    print(f"Found in method: {ret}")
    return ret

def validate_input(json_msg: str):
    set_of_keys_in_msg = set(json_msg.keys())
    set_of_keys_in_model = set(Opportunity.model_fields.keys())

    # Remove id to allow comparison
    set_of_keys_in_model.remove("id")

    if set_of_keys_in_msg != set_of_keys_in_model:
        print(f"Keys don't match ! You gave me {set_of_keys_in_msg} and I wanted {set_of_keys_in_model}")
        return False

    return True