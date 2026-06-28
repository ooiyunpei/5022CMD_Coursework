import multiprocessing
import time


# Function to calculate factorial
def factorial(n):
    # perf_counter_ns() is the best choice for high-resolution benchmarking
    start = time.perf_counter_ns()

    result = 1
    for i in range(1, n + 1):
        result *= i

    end = time.perf_counter_ns()

    # Return a tuple of (result, timestamps)
    return result, (start, end)


def run_multiprocess_round(pool):
    numbers = [50, 100, 200]

    # pool.map automatically distributes the numbers to the worker processes,
    raw_results = pool.map(factorial, numbers)

    # Unpack the results using list comprehensions
    results = [item[0] for item in raw_results]
    timestamps = [item[1] for item in raw_results]

    # Compute total time based on the inner timestamps
    earliest_start = min(t[0] for t in timestamps)
    latest_end = max(t[1] for t in timestamps)
    total_time = latest_end - earliest_start

    return total_time, results


def main():
    rounds = 10
    times = []

    print("=== PYTHONIC MULTIPROCESSING FACTORIAL (10 ROUNDS) ===\n")

    # Create the Pool ONCE and use a context manager (with statement)
    # to ensure it is cleanly closed and joined at the end.
    with multiprocessing.Pool(processes=3) as pool:
        for r in range(1, rounds + 1):
            total_time, results = run_multiprocess_round(pool)
            times.append(total_time)

            print(f"--- Round {r} ---")
            print(f"50!  = {results[0]}")
            print(f"100! = {results[1]}")
            print(f"200! = {results[2]}")
            print(f"Time Taken (ns): {total_time}\n")

    average_time = sum(times) / len(times)

    print("=== SUMMARY ===")
    for i, t in enumerate(times, 1):
        print(f"Round {i}: {t} ns")

    print(f"\nAverage Time Across 10 Rounds: {average_time:.2f} ns")


if __name__ == "__main__":
    main()