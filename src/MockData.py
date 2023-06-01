import time
import datetime
import numpy as np


class MockData():
    def __init__(self) -> None:
        self.time = self.random_time()
        self.now = datetime.datetime.now()
        self.pickup_time = np.random.randint(8, 20)
        self.user = self.random_user()
        self.provider = self.random_provider()
        self.food_type = np.random.choice(["breakfast", "lunch", "groceries", "bakery"])

    def random_time(self) -> time:
        hour = np.random.randint(0, 24)
        minutes = np.random.randint(0, 60)
        return datetime.datetime.strptime(f'{hour}:{minutes}', '%H:%M').time()

    def random_user(self) -> str:
        # TODO
        return "Piotr Berda"

    def random_provider(self) -> str:
        # TODO
        return "Bar Chwirot"
