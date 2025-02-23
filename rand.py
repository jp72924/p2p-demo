import random

def generate_random_numbers(start=0, end=100, count=1, as_int=True):
    """
    Generate random numbers within a specified range.

    Parameters:
        start (int or float): The lower bound of the range (inclusive).
        end (int or float): The upper bound of the range (exclusive for floats, inclusive for ints).
        count (int): The number of random numbers to generate.
        as_int (bool): If True, generate integers; if False, generate floating-point numbers.

    Returns:
        list: A list of random numbers.
    """
    if as_int:
        # Generate random integers
        return [random.randint(start, end) for _ in range(count)]
    else:
        # Generate random floating-point numbers
        return [random.uniform(start, end) for _ in range(count)]

# Example usage
if __name__ == "__main__":
    # Generate 5 random integers between 1 and 10
    random_integers = generate_random_numbers(start=1, end=10, count=5, as_int=True)
    print(f"Random Integers: {random_integers}")

    # Generate 3 random floating-point numbers between 0.0 and 1.0
    random_floats = generate_random_numbers(start=0.0, end=1.0, count=3, as_int=False)
    print(f"Random Floats: {random_floats}")