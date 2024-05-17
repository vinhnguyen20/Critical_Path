from typing import Any
import pandas as pd

import numpy as np
import random


def calculateCp(tam: pd.DataFrame):
#Varible New Fit C
    new_fit_c = []

    # tam = pd.read_excel('RESULT_MIN_Z.xlsx')
    extracted_data = pd.DataFrame(columns=["Min_Z"])
    extracted_data = pd.concat([extracted_data, pd.DataFrame(tam)], ignore_index = True)
    #Varible F
    F = sum(extracted_data['Min_Z'])

    numpy_array = extracted_data.values


    for i in range(len(numpy_array)):
        new_fit_c.append(1 - (numpy_array[i] / F))


    #---Varible p(c)
    sum_new_fit_c = sum(new_fit_c)
    p = []
    for i in range(len(numpy_array)):
        p.append((new_fit_c[i] / sum_new_fit_c))
    # print(p)

    #---Varible cp(c)
    cp_c = []
    for i in range(len(numpy_array)):
        tam_tinh = 0
        for j in range(int(i) + 1):
            tam_tinh = tam_tinh + p[j]
        cp_c.append(tam_tinh)

    # for i in range(len(numpy_array)):
    #     print(cp_c[i])

    return cp_c


# calculateCp()