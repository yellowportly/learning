from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from orm.operations import find_by_opportunity_id_async, do_update_from_object, find_all_opportunities
from orm.classes import Opportunity, OpportunityDataClass


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/opportunity/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: str):
    opportunity_in_db = await find_by_opportunity_id_async(opportunity_id)

    # Copy matching fields into response object
    response_opportunity = Opportunity(**opportunity_in_db.__dict__)
    return response_opportunity


@app.get("/opportunities", response_model=List[Opportunity])
async def get_all_opportunities():
    opps = find_all_opportunities()
    return opps


@app.put("/opportunity", status_code=200)
async def upsert_opportunity(request_opportunity: Opportunity, response: Response):
    found_opportunity = await find_by_opportunity_id_async(request_opportunity.opportunity_id)

    if found_opportunity is None:
        new_opportunity_for_insert = OpportunityDataClass(**request_opportunity.__dict__)
        newly_found_opportunity = do_update_from_object(new_opportunity_for_insert)
    else:
        # opportunity_for_update = deepcopy(request_opportunity)
        opportunity_ready_for_update = OpportunityDataClass(**found_opportunity.__dict__)
        opportunity_to_update = opportunity_ready_for_update.model_copy(update=request_opportunity.__dict__, deep=True)

        newly_found_opportunity = do_update_from_object(opportunity_to_update)

        if newly_found_opportunity is None:
            response.status_code = 404
            return None

    return newly_found_opportunity
