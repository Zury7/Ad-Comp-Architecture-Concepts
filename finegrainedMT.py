import threading
import time

def task(thread_id):
    print(f"Thread {thread_id} starting.")
    time.sleep(0.1)  # Simulating fine-grained task
    print(f"Thread {thread_id} finished.")

def fine_grained_multithreading():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=task, args=(i,))
        threads.append(thread)
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

fine_grained_multithreading()
