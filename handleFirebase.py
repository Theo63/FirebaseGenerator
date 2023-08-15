import json
import os
import JsonDBgenerator


#########get json database in one file ###
# with open("dummy_data.json", "r") as f:
#     print("reading dummy data")
#     file_contents = json.load(f)
#     print("gonna set")
# ref.set(file_contents)
# print("set ok")

def post_json_files(ref):
    ###### SET to firebase
    # Get json files in social media folder
    cwd = os.getcwd()  # Get the current working directory (cwd)
    directory = cwd + "/largeSocialDBJson"
    files = os.listdir(directory)
    index = 0
    while index < len(files):
        filename = files[index]
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as f:
                print("reading file " + filename)
                file_contents = json.load(f)
            ref.child(os.path.splitext(filename)[0]).set(
                file_contents)  # get the filename as first layer of tree and assign json data as its children
        index += 1


def deleteNode(ref, node):
    specific_entry_ref = ref.child(node)
    specific_entry_ref.delete()


####drop database#####
# deleteDB()
#
# ref.delete()


def writeUser(ref):
    # Reference to the 'users' node
    users_ref = ref.child('users')

    # Get a snapshot of the user data
    users_snapshot = users_ref.get()
    if users_snapshot:
        # Iterate through the user data and find the maximum user ID
        last_user_id = max([int(user['user_id']) for user in users_snapshot])
        print("\nGenerating User ID:", last_user_id, "\n")
    else:
        print("No user data available.")

    new_user = JsonDBgenerator.generate_user(int(last_user_id) + 1)
    userFile = "largeSocialDBJson/userEntry" + str(last_user_id + 1) +".json"
    with open(userFile, "w") as json_file:
        json.dump(new_user, json_file, indent=4)
    directory = os.getcwd()
    with open(os.path.join(directory, userFile)) as f:
        file_contents = json.load(f)
    users_ref.child(str(last_user_id)).set(
        file_contents)  # get the filename as first layer of tree and assign json data as its children

    os.remove(userFile)
