import random
from typing import Dict

def generate_random_actors(num_actors: int, pubs: list[str]):
    movement_number = { pub: 0 for pub in pubs }

    for _ in range(num_actors):
        random_pub = random.choice(pubs)
        movement_number[random_pub] += 1

    return movement_number

def generate_random_business(pubs: list[str]) -> Dict[str, int]:
    revenues = { pub: random.randrange(0, 1000) for pub in pubs }
    return revenues