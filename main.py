from copy import deepcopy
from fastapi import FastAPI, Response
from typing import List

from orm.operations import find_by_opportunity_id_async, do_update_from_object, find_all_opportunities
from orm.classes import Opportunity

app = FastAPI()


@app.get("/opportunity/{opportunity_id}")
async def get_opportunity(opportunity_id: str):
    opp = await find_by_opportunity_id_async(opportunity_id)
    return opp


@app.get("/opportunities", response_model=List[Opportunity])
async def get_all_opportunities():
    opps = find_all_opportunities()
    return opps


@app.put("/opportunity", status_code=200)
async def upsert_opportunity(request_opportunity: Opportunity, response: Response):
    found_opportunity = await find_by_opportunity_id_async(request_opportunity.opportunity_id)

    if found_opportunity is None:
        newly_found_opportunity = do_update_from_object(request_opportunity)
    else:
        request_opportunity_with_id = deepcopy(request_opportunity)
        request_opportunity_with_id.id = found_opportunity.id

        newly_found_opportunity = do_update_from_object(request_opportunity_with_id)

        if newly_found_opportunity is None:
            response.status_code = 404
            return None

    return newly_found_opportunity
