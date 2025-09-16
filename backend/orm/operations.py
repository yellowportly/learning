from typing import List

from orm.classes import Opportunity, opportunity_repo, OpportunityDataClass

# Used by FastAPI upsert
def do_update_from_object(request_opportunity: OpportunityDataClass) -> OpportunityDataClass:
    print(f"About to save: {request_opportunity}")
    opportunity_repo.save(request_opportunity)
    return find_by_opportunity_id(opportunity_id=request_opportunity.opportunity_id)

# FastAPI upsert
async def do_put_or_post(request_opportunity: Opportunity):
    found_opportunity = await find_by_opportunity_id_async(request_opportunity.opportunity_id)

    if found_opportunity is None:
        new_opportunity_for_insert = OpportunityDataClass(**request_opportunity.__dict__)
        newly_found_opportunity = do_update_from_object(new_opportunity_for_insert)
    else:
        # opportunity_for_update = deepcopy(request_opportunity)
        opportunity_ready_for_update = OpportunityDataClass(**found_opportunity.__dict__)
        opportunity_to_update = opportunity_ready_for_update.model_copy(update=request_opportunity.__dict__, deep=True)

        newly_found_opportunity = do_update_from_object(opportunity_to_update)
    return newly_found_opportunity

async def find_by_opportunity_id_async(opportunity_id: str) -> OpportunityDataClass:
    return find_by_opportunity_id(opportunity_id)

def find_all_opportunities() -> List[OpportunityDataClass]:
    opportunities = opportunity_repo.get_collection().find()
    return opportunities

def find_by_opportunity_id(opportunity_id: str) -> OpportunityDataClass:
    ret = opportunity_repo.find_one_by({"opportunity_id": opportunity_id})
    print(f"Looking for: {opportunity_id} Found in method: {ret}")
    return ret

def delete_by_opportunity_id(opportunity: OpportunityDataClass) -> None:
    opportunity_repo.delete_by_id(opportunity.id)
