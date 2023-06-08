import time
import datetime
import numpy as np
import random

FILENAME = "./data/restaurants.txt"


class MockData:
    def __init__(self, time, pickup_time, provider, food_type) -> None:
        self.time = time
        self.now = datetime.datetime.now()
        self.pickup_time = pickup_time
        self.provider = provider
        self.food_type = food_type

    def __str__(self) -> str:
        return f"{self.time} {self.now} {self.pickup_time} {self.provider} {self.food_type}"


def random_time() -> time:
    hour = np.random.randint(0, 24)
    minutes = np.random.randint(0, 60)
    return datetime.datetime.strptime(f"{hour}:{minutes}", "%H:%M").time()


def get_random_providers(n: int) -> str:
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        random_lines = random.choices(lines, k=n)
        random_providers = [line.strip() for line in random_lines]
    return random_providers


def create_mock_data(n: int) -> list[MockData]:
    random_providers = get_random_providers(n)
    items = []
    for i in range(n):
        time = random_time()
        pickup_time = np.random.randint(8, 21)
        provider = random_providers[i]
        food_type = np.random.choice(["breakfast", "lunch", "groceries", "bakery"])
        items.append(MockData(time, pickup_time, provider, food_type))
    return items
