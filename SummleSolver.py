from collections import deque

def solve_summle():
    print("--- Summle Solver ---")
    try:
        goal = int(input("Enter the Goal number: "))
        nums_raw = input("Enter the 6 numbers (separated by spaces): ")
        numbers = [int(x) for x in nums_raw.split()]
        
        if len(numbers) != 6:
            print("Error: You must provide exactly 6 numbers.")
            return
    except ValueError:
        print("Error: Please enter valid integers.")
        return

    # Queue stores: (current_numbers_tuple, path_of_steps)
    # Using a tuple for numbers so it can be hashed in the 'visited' set
    queue = deque([(tuple(sorted(numbers)), [])])
    visited = set()
    visited.add((tuple(sorted(numbers)), 0))

    while queue:
        current_nums, path = queue.popleft()

        # Check if goal is reached
        if goal in current_nums:
            print(f"\nSuccess! Found a {len(path)}-step solution:")
            for i, step in enumerate(path, 1):
                print(f"Step {i}: {step}")
            return

        # Stop if we hit the Summle 5-step limit
        if len(path) >= 5:
            continue

        # Try every combination of two numbers
        for i in range(len(current_nums)):
            for j in range(i + 1, len(current_nums)):
                a, b = current_nums[i], current_nums[j]
                
                # Create a list of remaining numbers
                remaining = list(current_nums)
                remaining.pop(j) # Pop larger index first to keep i valid
                remaining.pop(i)

                # Try all 4 operations
                possible_ops = []
                possible_ops.append(("+", a + b))
                if a * b != 0: # Avoid multiplying by 0 if applicable
                    possible_ops.append(("*", a * b))
                
                # Subtraction (must result in positive integer)
                if a - b > 0: possible_ops.append(("-", a - b))
                if b - a > 0: possible_ops.append(("-", b - a))
                
                # Division (must result in integer)
                if b != 0 and a % b == 0: possible_ops.append(("/", a // b))
                if a != 0 and b % a == 0: possible_ops.append(("/", b // a))

                for op, res in possible_ops:
                    # Ignore redundant operations like x * 1 or x / 1
                    if (op == "*" or op == "/") and (a == 1 or b == 1):
                        continue
                        
                    new_state = tuple(sorted(remaining + [res]))
                    if (new_state, len(path) + 1) not in visited:
                        visited.add((new_state, len(path) + 1))
                        
                        # Determine step formatting
                        if op in ["+", "*"]:
                            step_str = f"{max(a, b)} {op} {min(a, b)} = {res}"
                        elif op == "-":
                            step_str = f"{max(a, b)} - {min(a, b)} = {res}"
                        else: # Division
                            num, den = (a, b) if (b != 0 and a % b == 0 and a // b == res) else (b, a)
                            step_str = f"{num} / {den} = {res}"
                            
                        queue.append((new_state, path + [step_str]))

    print("\nNo solution found within 5 steps.")

if __name__ == "__main__":
    solve_summle()
