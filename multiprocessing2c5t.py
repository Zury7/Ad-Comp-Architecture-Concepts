import multiprocessing
import time

def task(thread_id):
    print(f"Thread {thread_id} starting on process {multiprocessing.current_process().name}.")
    time.sleep(1)  # Simulating some work
    print(f"Thread {thread_id} finished on process {multiprocessing.current_process().name}.")

def multiprocessing_simulation():
    # Set the number of processes to 2 (simulating 2 cores)
    num_cores = 2
    threads = 5  # We have 5 threads to run

    # Create a pool of 2 workers (simulating 2 cores)
    with multiprocessing.Pool(processes=num_cores) as pool:
        pool.map(task, range(threads))

multiprocessing_simulation()
