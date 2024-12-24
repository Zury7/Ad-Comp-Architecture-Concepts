import threading
import time

def task(thread_id):
    print(f"Thread {thread_id} starting.")
    time.sleep(1)  # Simulating coarse-grained task
    print(f"Thread {thread_id} finished.")

def coarse_grained_multithreading():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=task, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

coarse_grained_multithreading()
