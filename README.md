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

## Examples for mongo
- switch to schema using `use example`
- find all data from a specific collection in schema using `db.opportunities.find()`
- remove all items `db.opportunities.deleteMany({})`
- payload for a PUT request `{"opportunity_id":"127","url":"http://fred","title":"job","industry":"Hello","application_text":"Hire me please","status":"waiting"}`
- calling misquitto_pub from docker exec session `mosquitto_pub -u user1 -P password1 -m '{"industry":"Hello", "opportunity_id":"127","url":"http://fred","title":"job","application_text":"Hire me","status":"waiting"}' -t "learning/topic/opportunity"`

