import random


def random_sum() -> int:
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"{a} + {b} = {a + b}"


if __name__ == "__main__":
    print(random_sum())
