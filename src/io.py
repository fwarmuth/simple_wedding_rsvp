# Functions regarding reading preset_data.py
# retrieve all the names from the dataset and put them into a list
def get_pids(source):
    pids = []
    for entry in source:
        pid = entry["id"]
        pids.append(pid)
    return sorted(pids)

# find the row that matches the id in the URL, retrieve group_name and people
def get_invitation_preset(source, id):
    for row in source:
        if id == str( row["id"] ):
            group_name = row["group_name"]
            people = row["people"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, group_name, people
    # return these if id is not valid - not a great solution, but simple
    return False, False, False
