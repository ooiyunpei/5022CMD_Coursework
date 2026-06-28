import threading
import time

# Function to calculate factorial
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def thread_task(n, results, index, timestamps):
    start = time.perf_counter_ns()

    results[index] = factorial(n)

    end = time.perf_counter_ns()

    timestamps[index] = (start, end)


def run_multithread_round():
    numbers = [50, 100, 200]
    results = [None] * 3
    timestamps = [None] * 3

    # Create threads (using wrapper)
    t1 = threading.Thread(target=thread_task, args=(numbers[0], results, 0, timestamps))
    t2 = threading.Thread(target=thread_task, args=(numbers[1], results, 1, timestamps))
    t3 = threading.Thread(target=thread_task, args=(numbers[2], results, 2, timestamps))

    # Start threads
    t1.start()
    t2.start()
    t3.start()

    # Wait for completion
    t1.join()
    t2.join()
    t3.join()

    # Compute total time based on thread timestamps
    earliest_start = min(t[0] for t in timestamps)
    latest_end = max(t[1] for t in timestamps)
    total_time = latest_end - earliest_start

    return total_time, results

def main():
    rounds = 10
    times = []

    print("=== MULTITHREADED FACTORIAL COMPUTATION (10 ROUNDS, t1/t2/t3) ===\n")

    for r in range(1, rounds + 1):
        total_time, results = run_multithread_round()
        times.append(total_time)

        print(f"--- Round {r} ---")
        print(f"50! = {results[0]}")
        print(f"100! = {results[1]}")
        print(f"200! = {results[2]}")
        print(f"Time Taken (ns): {total_time}\n")

    average_time = sum(times) / len(times)

    print("=== SUMMARY ===")
    for i, t in enumerate(times, 1):
        print(f"Round {i}: {t} ns")

    print(f"\nAverage Time Across 10 Rounds: {average_time} ns")

if __name__ == "__main__":
    main()