from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from starlette import status

from orm.operations import find_by_opportunity_id_async, do_update_from_object, find_all_opportunities, \
    delete_by_opportunity_id, do_put_or_post
from orm.classes import Opportunity, OpportunityDataClass


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/opportunity/{opportunity_id}", status_code = 200, response_model=Opportunity)
async def get_opportunity(opportunity_id: str) -> Opportunity:
    opportunity_in_db = await find_by_opportunity_id_async(opportunity_id)

    if opportunity_in_db is None:
        raise HTTPException(status_code=404)

    # Copy matching fields into response object
    response_opportunity = Opportunity(**opportunity_in_db.__dict__)
    return response_opportunity


@app.get("/opportunities", response_model=List[Opportunity])
async def get_all_opportunities():
    opps = find_all_opportunities()
    return opps

@app.delete("/opportunity/{opportunity_id}", status_code = status.HTTP_200_OK)
async def delete_opportunity(opportunity_id: str, response: Response):
    found_opportunity = await find_by_opportunity_id_async(opportunity_id)

    if found_opportunity is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    delete_by_opportunity_id(found_opportunity)
    return


@app.put("/opportunity", status_code=200)
async def update_opportunity(request_opportunity: Opportunity):
    newly_found_opportunity = await do_put_or_post(request_opportunity)

    return newly_found_opportunity


@app.post("/opportunity", status_code=200)
async def insert_opportunity(request_opportunity: Opportunity):
    newly_found_opportunity = await do_put_or_post(request_opportunity)

    return newly_found_opportunity
