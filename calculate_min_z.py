from gamspy import Container, Set, Alias, Parameter, Variable, Equation, Model, Sum, Sense
import numpy as np
import sys
import pandas as pd
import os


def calculateMinZ(H = 2300, K_n: int = 0, extracted_data: pd.DataFrame = None ):
    m = Container()

    #-----------------------------------------Model sets and parameters---------------------------------
    activity = Set(container=m, name="sites", records=np.array([i for i in range(1, len(extracted_data["Activity"]) + 1)]))
    area = Set(container=m, name="mills", records=["value"])


    C_ij = Parameter(
        container=m, name="C_ij", domain=activity, records=np.array([float(i) for i in (extracted_data["C_ij"])])
    )

    max_S = Parameter(
        container=m, name="max_S", domain=activity, records=np.array([int(i) for i in (extracted_data["Max_S"])])
    )

    min_S = Parameter(
        container=m, name="min_S", domain=activity, records=np.array([int(i) for i in (extracted_data["Min_S"])])
    )


    #--------------------------------------------Constant-------------------------------------------
    x = Variable ( container = m , name = "d" , domain = activity , type = "positive" )

    e1 = Equation ( container = m , name = "eq1" , domain = activity )
    e1[ activity ] = x[ activity ] >= min_S[ activity ]

    e2 = Equation ( container = m , name = "eq2" , domain = activity )
    e2[ activity ] = x[ activity ] <= max_S[ activity ]


    #----------------------------------------------Objectivve function---------------------------------------
    Z = Sum([activity], H * x[activity]) + Sum([activity], C_ij[[activity]] * ( max_S[ activity ] - x[activity]))

    ans = Model ( container = m , name = "ans" , equations = m . getEquations () , problem = "LP" , sense =
    Sense . MIN , objective = Z )

    ans.solve()

    sum_Tn_sum = sum(x.records.level)

    return [ans.objective_value + K_n, sum_Tn_sum]

def convertMinZToDataFrame(result_object):
    res_fi = pd.DataFrame(result_object, columns = ['Min_Z'])
    return res_fi

def extractMinZToExcel(data: pd.DataFrame, columns):

    data.to_excel('RESULT_MIN_Z.xlsx',  index=False)

def extractDataMinZToExcel(data: []): 
    # print(data)
    file_name = 'RESULT_MIN_Z.xlsx'
    if os.path.exists(file_name) == False:
        df = pd.DataFrame(data,
                    columns=['Crashing duration','Min_Z', 'Normal Duration'])
        df.to_excel(file_name,  index=False)
    else:
        old_df = pd.read_excel(file_name)
        new_df = pd.DataFrame(data,
                    columns=['Crashing duration','Min_Z', 'Normal Duration'])
        merge_df = pd.concat([old_df, new_df])
        merge_df.to_excel(file_name,  index=False)


def addItemMinZ(tam_df, result_object):
    columns=['Crashing_Duration','Min_Z','Normal_Duration']
    res_fi = pd.DataFrame(result_object.reshape(-1, len(result_object)),columns=columns)
    tam_df = pd.concat([tam_df,res_fi],ignore_index = True)
    return tam_df

def performCalculateMinZ(tam: pd.DataFrame, df_individual, H):
    extracted_data = pd.DataFrame(columns=["Activity" , "C_ij" , "Max_S" , "Min_S"])
    extracted_data = pd.concat([extracted_data, pd.DataFrame(tam)], ignore_index = True)
           
    K_n = df_individual['Cost_of_normal_model'].sum()

    res = calculateMinZ(H = H, K_n=K_n, extracted_data=extracted_data)
    return res 

def performCalculateTotalTime(tam: pd.DataFrame, df_individual):
    return df_individual['Cost_of_normal_model'].sum()
    
def performCalculateMaxS(tam: pd.DataFrame, df_individual):
    return tam['Max_S'].sum()


def performCalculateTotalTimeTn(tam: pd.DataFrame, df_individual):
    Total_time_Tn = df_individual['Duration_of_normal_model'].sum()
    return Total_time_Tn

#-----------------------------------------Read data from excel---------------------------------------    
# result_object = [] 
# nDesiredIndividual = 5
# for index in range(nDesiredIndividual): 
#     PREFIX_FILE_NAME_IN = "FILE_MIN_Z_"
#     PREFIX_FILE_NAME_IN_INDIVIDUAL = "INDIVIDUAL_"
#     SUFFIX_FILE_NAME_IN = index + 1

#     file_name_out = PREFIX_FILE_NAME_IN + str(SUFFIX_FILE_NAME_IN) + '.xlsx'  
#     tam = pd.read_excel(file_name_out)

#     individual_file_name_out = PREFIX_FILE_NAME_IN_INDIVIDUAL + str(SUFFIX_FILE_NAME_IN) + '.xlsx'
#     df_individual = pd.read_excel(individual_file_name_out)

#     res = performCalculateMinZ(tam, df_individual)
    
#     result_object.append(res)


# extractMinZToExcel(result_object)
