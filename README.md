## Project
Opportunity management

Simple CRUD application to manage data around opportunities

## Objective
API as an MVP and then possibly a f/end if time allows

## Learning
- Python modules and how they interact
- Python data management and manipulation
- Use of pydantic module for ORM
- Use of mongo db

## Existing tech I know about
Docker for managing containers
- Settingup docker-compose with images
- Persistence of data
- Creation of schemas/collections/terminology in Mongo


## Databases
- opportunity
- contents
  - id
  - opportunity_id
  - url
  - title
  - industry
  - application text (free form)
  - status

## Issues
-  Encountered "cannot import name SON from bson" when running
  - had to run `poetry remove bson`
  - had to run `poetry remove pydantic-mongo`
  - had to run `poetry add pydantic-mongo`
  - resolved issue

