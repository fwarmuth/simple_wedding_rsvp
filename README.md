# RSVP app
App handles data collection from invitations and stores them in a `sqllite` database. Each invitation has a `unique ID` which is used for identification, as well as for authentication.

# How to:
- fill `unique_ids.txt` with random ids, row separated. 
- Create `preset_data.py` holding preset data for each unique id, which is used as initial values if invitation is not already in the database.
- Run `createdb.py` to create `rsvp.db` database with the right tables/columns.
- Done, run the docker.
