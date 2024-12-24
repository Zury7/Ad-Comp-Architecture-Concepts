import multiprocessing
import time


def task(thread_id):
    print(f"Thread {thread_id} starting.")
    time.sleep(0.5)  # Simulating task
    print(f"Thread {thread_id} finished.")

def simultaneous_multithreading():
    processes = []
    for i in range(5):
        process = multiprocessing.Process(target=task, args=(i,))
        processes.append(process)
        process.start()

    # Join processes
    for process in processes:
        process.join()

simultaneous_multithreading()
