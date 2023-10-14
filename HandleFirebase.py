import json
import os
import random
import sys
import time
from faker import Faker
import JsonDBgenerator

threadTimes = {}


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


def writeUser(thread_index, ref):
    # Reference to the 'users' node
    users_ref = ref.child('users')

    # Get a snapshot of the user data
    users_snapshot = users_ref.get()
    if users_snapshot:
        # Iterate through the user data and find the maximum user ID
        last_user_id = max([int(user['user_id']) for user in users_snapshot])
        print("\nGenerating User ID:", last_user_id + thread_index, "\n")
    else:
        print("No user data available.")

    new_user = JsonDBgenerator.generate_user(int(last_user_id) + thread_index + 1)
    userFile = "largeSocialDBJson/userEntry" + str(last_user_id + thread_index) + ".json"
    with open(userFile, "w") as json_file:
        json.dump(new_user, json_file, indent=4)
    directory = os.getcwd()
    with open(os.path.join(directory, userFile)) as f:
        file_contents = json.load(f)
    users_ref.child(str(int(last_user_id) + thread_index)).set(
        file_contents)  # get the filename as first layer of tree and assign json data as its children

    os.remove(userFile)


def readUser(ref):
    users_ref = ref.child('users')
    users_snapshot = users_ref.get()
    randomUser = users_snapshot[random.randint(0, len(users_snapshot))]
    try:
        print(f"Client {randomUser}")

    except Exception as e:
        print(f"Client {randomUser} encountered an error: {e}")


# testing scenario
# Function to search for a user by username
def searchUsername(ref):
    # Reference to the Firebase database node where your users are stored
    users_ref = ref.child('users')
    username = JsonDBgenerator.fake.user_name()
    # Query the database to find the user with the given username
    query = users_ref.order_by_child('username').equal_to(username).get()
    calculate_file_size(query, "search")
    if query:
        # The query is a dictionary of user data, so you can loop through it
        for user_id, user_data in query.items():
            print(f"---Found User with ID: {user_id} Username: {user_data['username']} Email: {user_data['email']}")
            # Add more fields as needed
    else:
        print(f"No user found with the username: {username}")


#  testing scenario
# Function to retrieve users with posts on a specific date
def get_posts_on_date_range(ref):
    # Reference to the Firebase Database
    start_date = "2023-03-15"
    end_date = "2023-03-30"
    privacy_setting = "Public"
    # Initialize an empty dictionary for users
    matching_posts = []

    # Reference to the "users" and "posts" nodes
    # users_ref = ref.child('users')
    posts_ref = ref.child('posts')

    # Record time
    start_time = time.time()
    # Query for posts with a timestamp on the specified date duration
    post_snapshot = posts_ref.order_by_child('timestamp').start_at(f'{start_date} 00:00:00').end_at(
        f'{end_date} 23:59:59').get()
    calculate_file_size(post_snapshot, " complex search")
    elapsed_time = time.time() - start_time

    # # If there are matching posts, retrieve the corresponding users
    # if post_snapshot:
    #     for post_id, post_data in post_snapshot.items():
    #         user_id = post_data.get('user_id')
    #
    #         # Retrieve the user's data
    #         user_data = users_ref.child(str(user_id[0])).get()
    #
    #         # Add the user to the result dictionary
    #         if user_data:
    #             username = user_data.get('username')
    #
    #             # Check if the username is in the list of usernames to filter
    #             if username in usernames_to_filter:
    #                 post_text = post_data.get('post_content')
    #                 post_date = post_data.get('timestamp')
    #                 matching_posts.append({
    #                     'username': username,
    #                     'post_text': post_text,
    #                     'post_date': post_date
    #                 })
    #
    # elapsed_time2 = time.time() - start_time

    # output_file_path = "results from " + start_date + " to " + end_date+".txt"
    #
    # corrected_elapsed_time = str(round(elapsed_time, 4))
    # results = []
    # for post_id, post_data in post_snapshot.items():
    #     user_id = post_data.get('user_id', '')
    #     date = post_data.get('timestamp', '')
    #     content = post_data.get('content', '')
    #
    #     # Append the extracted data to the results list
    #     results.append({
    #         'user_id': user_id,
    #         'date': date,
    #         'content': content
    #     })
    # # Open the file for writing
    # with open(output_file_path, 'w') as file:
    #     # Write the results to the file
    #     file.write(f"Elapsed time for date filtering: {corrected_elapsed_time}\nElapsed time for joining with users {corrected_elapsed_time}\n\n")
    #     file.write(f"Data size (bytes) for filtering: {data_size_bytes}\n\n")
    #     file.write(f"For posts from: {start_date} until: , {end_date}, \n\n")
    #     for result in results:
    #         file.write(f"User ID: {result['user_id']}, Date: {result['date']}, Content: {result['content']}\n")
    #
    # # Inform the user that the results have been saved
    # print("Results have been saved to", output_file_path)
    # print("Elapsed time: ", elapsed_time)


# testing scenario
def update_username(ref):
    try:
        # Reference the specific user by their user_id
        users_ref = ref.child('users')

        # Generate a random user index between 0 and num_users - 1
        random_user_index = random.randint(0, 10000 - 1)

        # Generate a random username using the Faker library
        fake = Faker()
        new_username = fake.user_name()

        # Reference the specific user by their index
        user_id = str(random_user_index)
        user_ref = users_ref.child(user_id)
        calculate_file_size(user_ref, "update ref")
        # Update the username for the random user
        user_ref.update({'username': new_username})

        update_data = ({'username': new_username})
        calculate_file_size(update_data, "update")
        print(f"Username updated for a random user with ID {user_id} to {new_username}")
    except Exception as e:
        print(f"Error updating username: {e}")


def bulkWritePage(thread_index, ref, last_page_id):
    # Reference to the 'users' node
    pages_ref = ref.child('pages')
    # print("\nGenerating hashtag: " + str(last_page_id))

    dummy_pages = JsonDBgenerator.generate_data(10, JsonDBgenerator.generate_page)
    userFile = "largeSocialDBJson/userEntry" + str(last_page_id + thread_index) + ".json"
    with open(userFile, "w") as json_file:
        json.dump(dummy_pages, json_file, indent=4)

    cwd = os.getcwd()  # Get the current working directory (cwd)
    directory = cwd + "/largeSocialDBJson"

    with open(os.path.join(directory, 'bulkPages.json')) as f:
        file_contents = json.load(f)
    pages_ref.child(str(int(last_page_id) + thread_index + 1)).set(
        file_contents)  # get the filename as first layer of tree and assign json data as its children
    calculate_file_size(file_contents, "bulkwriting")
    os.remove(userFile)


def calculate_file_size(file_contents, operation):
    # Serialize the data to JSON
    data_json = json.dumps(file_contents)
    # Calculate the payload size in bytes
    payload_size = len(data_json)
    print(f"{operation} Payload size in bytes: {payload_size}")
