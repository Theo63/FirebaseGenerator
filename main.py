from unittest import case

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import HandleFirebase
from JsonDBgenerator import generate_and_save_data
import HandleFirebase as handleFirebase
import StressTest

cred = credentials.Certificate("firebase_key/social-network-cfa25-firebase-adminsdk-1up9x-40571cb5c4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://social-network-cfa25-default-rtdb.europe-west1.firebasedatabase.app"})
ref = db.reference("/")

# StressTest.stressing(ref)

choice = " "
menu = [" ","1","2","3","4","5"]
while choice in menu:
    choice = input(
        " Press 1 to get json files in social media folder\n press 2 to write json files to Firebase,"
        "\n press 3 to search for last user,\n press 4 to delete a node,\n press 5 to stress test db,"
        "\n press 6 to perform post filtering,\n"
        "press anything else to exit:\n ")
    if choice == "1":
        population = input("Select population for nodes: ")
        print("Getting json files in social media folder")
        generate_and_save_data(int(population))
    elif choice == "2":
        print("Writing json files to Firebase")
        handleFirebase.post_json_files(ref)
    elif choice == "3":
        print("just searching for last user id")
        handleFirebase.writeUser(1,ref)
    elif choice == "4":
        for key in ref.get().keys():
            print(key)
        node = input("Enter the node you want to delete from Firebase: ")
        handleFirebase.deleteNode(ref, node)
    elif choice == "5":
        # userThreads = input("select the number of threads you want to test: ")
        StressTest.stressing(ref, 10)
        # StressTest.stressing(ref, 100)
        # StressTest.stressing(ref, 200)
    elif choice == "6":
        HandleFirebase.bulkWritePage(0, ref)
    else:
        print("exiting")

#
# Reference to the Firebase database root
# ref = db.reference()
#
# # Load data from Firebase
# users_ref = ref.child('users')
# users_data = users_ref.get()
#
# if users_data is None:
#     print("No data found in the 'users' path.")
# else:
#     # Iterate through each user in the list
#     for user in users_data:
#         print("User ID:", user["user_id"])
#         print("Username:", user["username"])
#         print("Fullname:", user["fullname"])
#         # Print other user attributes
#         print()  # Add an empty line between users


#
# ####### Load Data with UPDATE###################
# choice = input(" Press 1 to get json files in social db")
# if choice == "1":
#     #Get json files in social media folder
#     cwd = os.getcwd()  # Get the current working directory (cwd)
#     directory = cwd + "/largeSocialDBJson"
#     files = os.listdir(directory)
#     index = 0
#     while index < len(files):
#         filename = files[index]
#         if filename.endswith('.json'):
#             with open(os.path.join(directory, filename)) as f:
#                 print("reading file " + filename)
#                 file_contents = json.load(f)
#                 id = 0
#             for i in range(0, len(file_contents), chunk_size):
#                 batch_data = file_contents[i:i + chunk_size]
#                 batch = {}
#                 # ref.child(os.path.splitext(filename)[0]).set(batch_data)  # get the filename as first layer of tree and assign json data as its children
#                 for j, item in enumerate(file_contents, start=len(ref.child(os.path.splitext(filename)[0]).get())):
#                     new_key = j  # Use the counter as the key  # Generate a new unique key
#                     batch[new_key] = item
#                 ref.child(os.path.splitext(filename)[0]).update(batch)
#         index += 1
