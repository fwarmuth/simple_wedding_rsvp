# functions to be used by the routes

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        # lowercase all the names for better searching
        name = row["id"]
        names.append(name)
    return sorted(names)

# find the row that matches the id in the URL, retrieve name and people
def get_actor(source, id):
    for row in source:
        if id == str( row["id"] ):
            group_name = row["group_name"]
            people = row["people"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, group_name, people
    # return these if id is not valid - not a great solution, but simple
    return "Unknown", "Unknown", ""

# find the row that matches the name in the form and retrieve matching id
def get_id(source, name):
    for row in source:
        # lower() makes the string all lowercase
        if name == row["id"]:
            id = row["id"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"


