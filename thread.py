import threading
import time

# Function that each thread will execute
def worker(thread_id, delay):
    print(f"Thread {thread_id} started.")
    for i in range(5):
        time.sleep(delay)  # Simulate some work by sleeping
        print(f"Thread {thread_id}: Working... ({i + 1}/5)")
    print(f"Thread {thread_id} finished.")

def main():
    threads = []
    
    # Create and start 3 threads
    for i in range(3):
        # Each thread gets a unique ID and a random delay
        thread = threading.Thread(target=worker, args=(i, i + 1))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads have finished execution.")

if __name__ == "__main__":
    main()