import threading
import time
import handleFirebase


database_lock = threading.Lock()
# Function to simulate a database operation
def perform_database_operation(thread_index, ref):
    with database_lock:
        print(f"Thread {thread_index} acquired the database lock.")
        handleFirebase.writeUser(ref)
        print(f"Thread {thread_index} completed.")


def stressing(ref, userThreads):
    # Create and start threads
    threads = []
    start = time.time()
    for i in range(userThreads):
        thread = threading.Thread(target=perform_database_operation, args=(i, ref))
        thread.start()
        threads.append(thread)
        # time.sleep(1) ## time in seconds

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    end = time.time()

    print("All threads completed in:"+str(end-start)+" seconds.")
