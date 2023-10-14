import threading
import time
import HandleFirebase
import PlotGenerator

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

threadTimes = {}
database_lock = threading.Lock()

newUserIndex = 0


def stressing(ref, userThreads):
    global newUserIndex  # we want to write to db with using ONLY WRITE operation thread number
    newUserIndex = 0
    global threads
    threads = []
    global userThreadsList
    userThreadsList = [[] for _ in range(5)]

    threadsCreatorList = []

    pages_ref = ref.child('pages')
    global last_page_id
    last_page_id = int(list(pages_ref.order_by_key().limit_to_last(1).get().keys())[0])

    # ----------------- This is the code for creating threads without splitting them to threads -------------------- #
    # userThreadsList = []
    # for i in range(userThreads):
    #     # Generate unique app names for each client
    #     app_name = f'app{i + 1}'
    #
    #     # Initialize Firebase Admin SDK for the client
    #     cred = credentials.Certificate("firebase_key/auth-social-network-489ae-firebase-adminsdk-gz5c0-e0419a6447.json")
    #     firebase_admin.initialize_app(cred, {
    #         'databaseURL': f'https://auth-social-network-489ae-default-rtdb.europe-west1.firebasedatabase.app'
    #     }, name=app_name)  # The name=app_name parameter is used to specify
    #     # a unique name for the Firebase app instance you are initializing
    #
    #     # Create a reference to the /data path for the client
    #     ref = db.reference(app=firebase_admin.get_app(name=app_name),
    #                        url=f'https://auth-social-network-489ae-default-rtdb.europe-west1.firebasedatabase.app/data')
    #
    #     userThreadsList.append((app_name, ref))
    #     print(app_name)
    # # Create and start threads
    # threads = []
    #
    # for i in range(len(userThreadsList)):
    #     # print(str(userThreadsList[i][0]) + ", "+ str(userThreadsList[i][1]))
    #     thread = threading.Thread(target=perform_database_operationSearch,
    #                               args=(i, userThreadsList[i][1]))  # i for thread(user) 1 for ref
    #     threads.append(thread)
    # ------------------------------------------------------------------------------------------------- #

    # create threads using 5 threads to perform the creation
    for threadno in range(5):
        threadCreator = threading.Thread(target=theadCreate,
                                         args=(threadno, userThreads, userThreadsList))  # i for thread(user) 1 for ref
        threadsCreatorList.append(threadCreator)
    #  start the thread creator threads
    for thread0 in threadsCreatorList:  # we start all threads together to make sure we get correct time response from db
        thread0.start()

    # Wait for all threads to complete
    for thread0 in threadsCreatorList:
        thread0.join()
        # time.sleep(1) ## time in seconds

    print("-----------------------Threads created, starting threads...------------------------")
    # all threads created are new to global variable threads
    for thread in threads:  # we start all threads together to make sure we get correct time response from db
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Clean up Firebase Admin SDK instances
    for k in range(5):
        for app_name, _ in userThreadsList[k]:
            try:
                firebase_admin.delete_app(firebase_admin.get_app(name=app_name))
            except Exception as e:
                print(app_name + "could not be deleted: " + str(e))

    sorted_dict = dict(sorted(threadTimes.items(), key=lambda item: item[1][2]))
    output_file_path = f"Time results for {userThreads} users.txt"
    with open(output_file_path, 'w') as file:
        for time in sorted_dict.keys():
            file.write(
                "Thread " + str(time) + " completed in : " + str(sorted_dict[time][2]) + " seconds. Operation: " + str(
                    sorted_dict[time][3]) + "\n")
    timeSort(threadTimes)
    PlotGenerator.plotCreator(sorted_dict)





# Function to simulate a database operation
def perform_database_operationWrite(thread_index, ref, users, col):
    writestart = time.time()
    tableIndex = int(col * (users / 5) + thread_index)
    threadTimes[tableIndex] = [writestart]

    global newUserIndex
    newUserIndex += 1  # we increment before starting because of threading (we don't know when thread will finish writeUser)
    HandleFirebase.bulkWritePage(newUserIndex - 1, ref, last_page_id)
    print(f"Thread {tableIndex} completed.")
    writeend = time.time()
    threadTimes[tableIndex].append(writeend)
    threadTimes[tableIndex].append(writeend - threadTimes[tableIndex][0])
    threadTimes[tableIndex].append("Write operation")


def perform_database_operationSearch(thread_index, ref, users, col):
    readstart = time.time()
    tableIndex = int(col * (users / 5) + thread_index)
    print(tableIndex)
    threadTimes[tableIndex] = [readstart]
    HandleFirebase.searchUsername(ref)
    print(f"Thread {tableIndex} completed.")
    readend = time.time()
    threadTimes[tableIndex].append(readend)
    threadTimes[tableIndex].append(readend - threadTimes[tableIndex][0])
    threadTimes[tableIndex].append("Search operation")


def perform_database_operationSearchFilter(thread_index, ref, users, col):
    readstart = time.time()
    tableIndex = int(col * (users / 5) + thread_index)
    print(tableIndex)
    threadTimes[tableIndex] = [readstart]
    HandleFirebase.get_posts_on_date_range(ref)
    print(f"Thread {tableIndex} completed.")
    readend = time.time()
    threadTimes[tableIndex].append(readend)
    threadTimes[tableIndex].append(readend - threadTimes[tableIndex][0])
    threadTimes[tableIndex].append("Search in date range operation")


def perform_database_update(thread_index, ref, users, col):
    readstart = time.time()
    tableIndex = int(col * (users / 5) + thread_index)
    print(tableIndex)
    threadTimes[tableIndex] = [readstart]
    HandleFirebase.update_username(ref)
    print(f"Thread {tableIndex} completed.")
    readend = time.time()
    threadTimes[tableIndex].append(readend)
    threadTimes[tableIndex].append(readend - threadTimes[tableIndex][0])
    threadTimes[tableIndex].append("Search in date range operation")


# ---------------function to sort all times collected
def timeSort(threadTimes):
    # PRINT TOTAL TIME ENLAPSED
    # MIN TIME
    min_value2 = float('inf')  # Initialize with positive infinity
    # Iterate through the keys and their associated values
    for key, values in threadTimes.items():
        value2 = values[0]  # Assuming value2 is always at index 1

        # Compare and update the minimum value2
        if value2 < min_value2:
            min_value2 = value2

    # print("Minimum value2 across all keys:", min_value2)
    # Initialize a variable to store the minimum value2
    max_value3 = float(0.0)  # Initialize with positive infinity
    # MAX TIME
    for key, values in threadTimes.items():
        value3 = values[1]  # Assuming value2 is always at index 1

        # Compare and update the minimum value2
        if value3 > max_value3:
            max_value3 = value3

    # print("Maximum value2 across all keys:", max_value3)
    print("---------  All threads completed in:" + str(max_value3 - min_value2) + " seconds.----------------")


# ------------ a function to create thrreads used for accesing thread creation
def theadCreate(threadno, userThreads, userThreadsList):
    # Calculate the start and end indices for the current thread
    start_index = threadno * (userThreads / 5)  # ---------threadno is the column number and userThreads/5 are the rows.
    end_index = (threadno + 1) * (userThreads / 5) - 1 if threadno < 5 - 1 else userThreads - 1

    # create different db references
    for i_big in range(int(start_index), int(end_index) + 1):
        # Generate unique app names for each client
        app_name = f'app{i_big + 1}'  # unique app names

        # Initialize Firebase Admin SDK for the client

        cred = credentials.Certificate(
            "firebase_key/social-network-cfa25-firebase-adminsdk-1up9x-40571cb5c4.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': f'https://social-network-cfa25-default-rtdb.europe-west1.firebasedatabase.app'
        }, name=app_name)  # The name=app_name parameter is used to specify
        # a unique name for the Firebase app instance you are initializing

        # Create a reference to the /data path for the client
        ref = db.reference(app=firebase_admin.get_app(name=app_name),
                           url=f'https://social-network-cfa25-default-rtdb.europe-west1.firebasedatabase.app/data')

        userThreadsList[threadno].append((app_name, ref))  # a list that contains lists of threads
        # print("Thread "+ str(threading.current_thread())+" creating "+ str(app_name))

    for i in range(len(userThreadsList[threadno])):
        # print(str(userThreadsList[threadno][i][0]) + ", "+ str(user5ThreadsList[threadno][i][1]))
        thread = threading.Thread(target=perform_database_operationWrite,
                                  args=(i, userThreadsList[threadno][i][1], userThreads,
                                        threadno))  # [threadno = col][i = for thread(user)] [1 = for ref value],

        # perform_database_operationSearchFilter , perform_database_operationSearch,
        # perform_database_operationWrite , perform_database_update

        threads.append(thread)
        # time.sleep(1) ## time in seconds

# def perform_database_operationRead(thread_index, ref):
#     readstart = time.time()
#     threadTimes[thread_index] = [readstart]
#     HandleFirebase.readUser(ref)
#     print(f"Thread {thread_index} completed.")
#     readend = time.time()
#     threadTimes[thread_index].append(readend)
#     threadTimes[thread_index].append(readend - threadTimes[thread_index][0])
#     threadTimes[thread_index].append("Read operation")
