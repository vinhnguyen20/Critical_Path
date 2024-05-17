import random
from Models import Individual
def perform_elistic(individuals: [Individual], random_individuals: [Individual]): 
    size = len(random_individuals)
    indices = random.choices(range(len(individuals)), k = size )
    print("SHOW ALL POSITION IN INDICES", indices)
    for i in range(0, len(indices)): 
        index = indices[i]
        individuals[index] = random_individuals[i]
    return individuals