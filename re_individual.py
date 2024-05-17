
import random


from Models import Individual



def select(cp: [] = [], old_individuals: [Individual] = None) -> [Individual]:
    MIN_RANDOM = 0
    MAX_RANDOM = 1 
    nRandomValue = len(cp)
    nGeneratedRandomValue = 1
    r_values = []

    if(cp is None or old_individuals is None or len(cp) == 0 or len(old_individuals) == 0):
        raise ValueError("Please provide cp and individuals")

    if(len(cp) != len(old_individuals)):
        raise ValueError("Please provide the number of cp  the same the number of individuals")

    while(nGeneratedRandomValue <= nRandomValue):
        r_value = random.uniform(MIN_RANDOM, MAX_RANDOM)
        r_values.append(r_value)
        nGeneratedRandomValue += 1

    new_individuals: [Individual] = []

    for r_value in r_values:
        # print(r_value)
        for j in range(0, len(cp)):
            if(j == 0):
               if(r_value <= cp[j]):
                    new_individuals.append(old_individuals[j]) 
                    pass

            else:
                if(cp[j - 1] <= r_value and r_value <= cp[j]):
                    new_individuals.append(old_individuals[j])
                    pass
    return new_individuals