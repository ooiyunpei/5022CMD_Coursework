import time

# Normal factorial function
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def main():
    numbers = [50, 100, 200]
    rounds = 10  # number of times we repeat the process
    times = []  # store execution time for each round

    print("=== NON-MULTITHREADED FACTORIAL COMPUTATION (10 ROUNDS) ===\n")

    for r in range(1, rounds + 1):
        print(f"--- Round {r} ---")
        start = time.perf_counter_ns()

        for num in numbers:
            result = factorial(num)
            print(f"{num}! = {result}")

        end = time.perf_counter_ns()
        elapsed = end - start
        times.append(elapsed)

        print(f"Time Taken (ns): {elapsed}\n")

    # Calculate average
    average_time = sum(times) / 10

    print("=== SUMMARY ===")
    for i, t in enumerate(times, 1):
        print(f"Round {i}: {t} ns")

    print(f"\nAverage Time Across 10 Rounds: {average_time} ns")

if __name__ == "__main__":
    main()