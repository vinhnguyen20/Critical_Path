from typing import Any
import pandas as pd
import PySimpleGUI as pg
import read_data
import critical_path
import cross_over
import calculate_min_z
from Models import Activity, ActivityManager, Individual, Model
import re_individual
from collections import deque
import elistic
import random
import datetime

path_df = 'Dat-thesis.xlsx'
df = pd.read_excel(path_df)

N_DESIRED_INDIVIDUALS = 50
N_ROUNDS = 3
CONST_H = 2300


def performIntializationPopulation():
    activities: [Activity] = read_data.getAllActivities(df)
    individuals: [Individual] = read_data.getAllIndividuals(nDesiredIndividual=N_DESIRED_INDIVIDUALS, activities=activities) 
    return individuals


def printIndividual(individual: Individual, individual_pos: int): 
    print('-----------------Individual-------------------------------------' + str(individual_pos))
    activities = individual.activities
    for activity in activities:
        print(activity.activity_number)

def performIndividual():
    pass
 
def evaluateObjectiveFunctionOfEachIndividual(individuals: [Individual]):
    res_minz = []
    result_min_z = []
    
    for individual in individuals:
        """
            Find critical path
        """
        df_for_critical_path = read_data.convertIndividualToDataFrameForCriticalPath(individual)
        # print(df_for_critical_path)
        activity_path = critical_path.find_path(df_for_critical_path)
        activity_path.reverse()
        activity_file = pd.DataFrame(activity_path) 
        df_for_min_z = critical_path.convertCriticalPathToDataFrameForMinZ(activity_file, df_for_critical_path)

        [min_z, sum_tn_sum] = calculate_min_z.performCalculateMinZ(df_for_min_z, df_for_critical_path, H = CONST_H)        
        res_minz.append(min_z)

        # total_time = calculate_min_z.performCalculateTotalTime(df_for_min_z, df_for_critical_path)
        max_s = calculate_min_z.performCalculateMaxS(df_for_min_z, df_for_critical_path)

        result_min_z_item = [sum_tn_sum, min_z, max_s]
        result_min_z.append(result_min_z_item)




def generateRandomPercentValue(numberOfIndividual: int = None, desiredPercent: float = None):

    MIN_RANDOM = 0
    MAX_RANDOM = 1
    
    if numberOfIndividual == None:
        raise ValueError('Please provide a number of individual')
    
    if(desiredPercent < 0 or desiredPercent > 1):
        raise ValueError('Please provide a desired between 0 and 1')

    numberOfDesiredIndividual = round(float(numberOfIndividual * desiredPercent))
    print(numberOfDesiredIndividual)
    if numberOfDesiredIndividual % 2 == 1:
        numberOfDesiredIndividual -= 1

    r_values = []

    nGeneratedDesiredIndividualCount = 1
    while(nGeneratedDesiredIndividualCount <= numberOfDesiredIndividual): 
        r_value = random.uniform(MIN_RANDOM, MAX_RANDOM * desiredPercent)
        r_values.append(r_value)

        nGeneratedDesiredIndividualCount += 1  

    return r_values 

def performSelectionOfIndividual():
    print('Step: Selection of Individual Solution')


    pass 

def performCrossOver():
    print('Step: Cross Over')
    pass

def performMutation():
    print('Step: Mutation') 
    pass

def perfromElitistStrategy():
    print('Step: Elistist Strategy')
    pass


"""
    Target: 
        1. Random select model activity in each individual
        2. From v1 and v2 -> selectModelOfActivity -> v1' and v2'
"""

def convertModeNumberOfIndividualToArray(individual: Individual):
    return individual['Mode_number'].to_numpy()

def convertArrayToModeNumberOfIndividual(individual: Individual):
    return 

def     selectModelOfIndividual(numpy_array_1: [], numpy_array_2: []):

    tam_index_1 = random.randint(2,int(len(numpy_array_1)/3))
    tam_index_2 = random.randint(int(len(numpy_array_1)*3/4), len(numpy_array_1)-2)

    # print('------------------------------------Value n------------------------------------------------')
    # print(tam_index_1)
    # print('------------------------------------Value m------------------------------------------------')
    # print(tam_index_2)

    n = tam_index_1
    m = tam_index_2

    #offering_root
    mid_offering_2 = numpy_array_2[n:m:]
    mid_offering_1 = numpy_array_1[n:m:]
    tam_offering_2 = []
    tam_offering_1 = []

    # print(mid_offering_2)

    #intermediate_individual_1
    stage_start_1 = numpy_array_1[:m:]
    stage_finish_1 = numpy_array_1[m::]
    intermediate_individual_1= []
    for i in range(len(stage_finish_1)):
        intermediate_individual_1.append(stage_finish_1[i])
    for i in range(len(stage_start_1)):
        intermediate_individual_1.append(stage_start_1[i])

    stage_start_2 = numpy_array_2[:m:]
    stage_finish_2 = numpy_array_2[m::]
    intermediate_individual_2 = []
    for i in range(len(stage_finish_2)):
        intermediate_individual_2.append(stage_finish_2[i])
    for i in range(len(stage_start_2)):
        intermediate_individual_2.append(stage_start_2[i])


    #-----------------------------Delete element not in middle offering------------------------------
    for i in range(len(mid_offering_1)):
        if (mid_offering_1[i] in intermediate_individual_2):
            intermediate_individual_2.remove(mid_offering_1[i])
        if (mid_offering_2[i] in intermediate_individual_1):
            intermediate_individual_1.remove(mid_offering_2[i])

    tam_offering_1 = intermediate_individual_1

    tam_offering_2 = intermediate_individual_2

    #----------------------------Create offering--------------------------------
    leng_1 = len(numpy_array_1) - m
    res_offering_1 = []
    res_offering_2 = []

    for i in range(leng_1, leng_1 + n):
        res_offering_2.append(tam_offering_2[i])
        res_offering_1.append(tam_offering_1[i])

    for i in range(len(mid_offering_2)):
        res_offering_2.append(mid_offering_1[i])
        res_offering_1.append(mid_offering_2[i])

    for i in range(leng_1):
        res_offering_2.append(tam_offering_2[i])
        res_offering_1.append(tam_offering_1[i])

    # print('------------------------------------Offering 1------------------------------------------------')
    # print(res_offering_1)
    # print('------------------------------------Offering 2------------------------------------------------')
    # print(res_offering_2)

    return [res_offering_1, res_offering_2]
    # #Độ phưc tap dang la dang la O(n)


def selectModeForMutation(numpy_array: []) -> []:
    # print('-----------------------------------------------------------------------------------------------------------------')


    # Bước này là mình chọn điểm cắt tương ứng 1 và 2
    tam_index_1 = random.randint(2,int(len(numpy_array)/3))
    tam_index_2 = random.randint(int(len(numpy_array)*2/3), len(numpy_array)-2)
    # print('------------------------------------Value n------------------------------------------------')
    # print(tam_index_1)
    # print('------------------------------------Value m------------------------------------------------')
    # print(tam_index_2)


    n = tam_index_1
    m = tam_index_2


    #tách activity thành 3 phần
    start_array: [int] = numpy_array[:n:]
    finish_array: [int] = numpy_array[m::]
    mid_array: [int] = numpy_array[m-1:n-1:-1]


    # #ghép lại file cuối
    res_file = []
    for i in range(len(start_array)):
        res_file.append(int(start_array[i]))

    for i in range(len(mid_array)):
        res_file.append(int(mid_array[i]))

    for i in range(len(finish_array)):
        res_file.append(int(finish_array[i]))

    return res_file

def performModelOfNoExistingIndividual():
    pass


def getNewModeOfIndividual(mode_number: int, activity: Activity) -> Model:
    models = activity.models
    for model in models:
        if model.model_number == mode_number:
            return model
    return None

def updateNewModeNumberOfIndividual(new_mode_numbers: [], individual: Individual):
    activities = individual.activities
    if len(new_mode_numbers) != len(activities):
        raise ValueError('the number of new modes must match the number of activities for each invididual')

    for i in range(0, len(activities)):
        activity = activities[i]
        models = activities[i].models
        new_mode_number = new_mode_numbers[i]

        if new_mode_number > len(models): 
            """
                Target: 
                    1. If 'new_mode' is greater than the number of models, then set defined mode to  1 
            """
            print('Resovle new mode in the activity of individual')        
            individual[i] = models[0]
        else: 
            newModel = getNewModeOfIndividual(new_mode_number, activity=activity)
            individual[i] = newModel


"""Taqget:
    1. the output of function is list of dataframe
    2. desiredGetPercent: determine the number of desired get individual from it output
"""
def getDesiredIndividualsWithDesiredPercent(individuals: {} = None, desiredGetPercent: float = 1, shouldEven: bool = False) -> {}:
    new_individuals: {} = {}
    if individuals is None: 
        raise ValueError('Please provide individuals')

    totalIndividuals = len(individuals)
    desiredTotalIndividuals = round(totalIndividuals * desiredGetPercent)

    if shouldEven:
        desiredTotalIndividuals = desiredTotalIndividuals - desiredTotalIndividuals % 2    

    individual_positions = [key for key in individuals.keys()]
    random.shuffle(individual_positions)
    desired_invidividual_positions = individual_positions[:desiredTotalIndividuals]
    for item_position in desired_invidividual_positions: 
        new_individuals[item_position] = individuals[item_position]

    return new_individuals 


def convertIndividualsToDict(individuals: [pd.DataFrame]) -> {}: 
    res = {}
    for i in range(0, len(individuals)):
        res[i] = individuals[i]
    return res 

def perform_evaluate_objective_function_of_each_individual(individuals: [Individual]):
    res_minz = []
    for individual in individuals:

        df_for_critical_path = read_data.convertIndividualToDataFrameForCriticalPath(individual)
        activity_path = critical_path.find_path(df_for_critical_path)
        activity_path.reverse()
        activity_file = pd.DataFrame(activity_path)
        df_for_min_z = critical_path.convertCriticalPathToDataFrameForMinZ(activity_file, df_for_critical_path)
        min_z = calculate_min_z.performCalculateMinZ(df_for_min_z, df_for_critical_path, H = CONST_H)
        res_minz.append(min_z)


    df_for_cross_over = calculate_min_z.convertMinZToDataFrame(res_minz)
    cp_c = cross_over.calculateCp(df_for_cross_over)

    cp_c = [item[0] for item in cp_c]

def perform_select_of_individuals_solution(cp_c: [], individuals: [Individual]) -> [Individual]:
    new_individuals = re_individual.select(cp = cp_c, old_individuals = individuals)
    return new_individuals

def perform_cross_over(individuals: {}):
    new_individuals: {} = getDesiredIndividualsWithDesiredPercent(individuals=individuals, desiredGetPercent= 0.8, shouldEven = True)

    keys = [key for key in new_individuals.keys()] 

    for i in range(0, len(keys), 2):
        individual_1 = new_individuals[keys[i]]
        individual_2 = new_individuals[keys[i + 1]]
    
        mode_number_of_individual_1 = convertModeNumberOfIndividualToArray(individual_1)
        mode_number_of_individual_2 = convertModeNumberOfIndividualToArray(individual_2)

        [new_mode_number_of_individual_1, new_mode_number_of_individual_2] = selectModelOfIndividual(mode_number_of_individual_1, mode_number_of_individual_2)

        individual_1['Mode_number'] = new_mode_number_of_individual_1
        individual_2['Mode_number'] =new_mode_number_of_individual_2

    return new_individuals


def perform_mutation(individuals: {}):
    new_individuals = getDesiredIndividualsWithDesiredPercent(individuals=individuals, desiredGetPercent=0.2, shouldEven=False)

    keys = [key for key in new_individuals.keys()] 
    individual = new_individuals[keys[0]]

    mode_number_of_individual = convertModeNumberOfIndividualToArray(individual)
    new_mode_number_of_individual = selectModeForMutation(mode_number_of_individual)
    individual['Mode_number'] = new_mode_number_of_individual

    return new_individuals


def perform_elistic(individuals: {} = None, random_individuals: {} = None):
    print(perform_elistic)

# Output: DataFrame
def getReplacedIndividuals(origin_individuals: {}, replaced_individual: {}) -> {}:
    new_individuals = origin_individuals.copy()
    
    for key in replaced_individual.keys():
        numpy_array = replaced_individual[key]['Number_of_mode'].to_numpy()
        mode_number = replaced_individual[key]['Mode_number'].to_numpy()
        
        for i in range(0, len(mode_number)):
            if mode_number[i] > numpy_array[i]:
                mode_number[i] = 1
                
        new_individuals[key] = replaced_individual[key] 
    
    return new_individuals


global savedInitIndividual
savedInitIndividual  = None


def printModeNumberOfIndividuals(individuals: {}):
    savedInitIndividuals = []
    for key in individuals.keys():
        individual = individuals[key]
        mode_numbers = individual['Mode_number'].to_numpy()
        savedInitIndividuals.append(mode_numbers)



def performRound(individuals: [Individual], index_round: int = None) -> [Individual]:

    # individuals: [Individual] = init_individuals()
    res_minz = []
    result_min_z = []

    savedAllIndividuals.extend(individuals)
 
    for individual in individuals:

        df_for_critical_path = read_data.convertIndividualToDataFrameForCriticalPath(individual)
        # print(df_for_critical_path)
        activity_path = critical_path.find_path(df_for_critical_path)
        activity_path.reverse()
        activity_file = pd.DataFrame(activity_path) 
        df_for_min_z = critical_path.convertCriticalPathToDataFrameForMinZ(activity_file, df_for_critical_path)


        [min_z, sum_tn_sum] = calculate_min_z.performCalculateMinZ(df_for_min_z, df_for_critical_path, H = CONST_H)        
        res_minz.append(min_z)

        # total_time = calculate_min_z.performCalculateTotalTime(df_for_min_z, df_for_critical_path)
        max_s = calculate_min_z.performCalculateMaxS(df_for_min_z, df_for_critical_path)

        result_min_z_item = [sum_tn_sum, min_z, max_s]
        result_min_z.append(result_min_z_item)
        

    calculate_min_z.extractDataMinZToExcel(result_min_z)
 
    df_for_cross_over = calculate_min_z.convertMinZToDataFrame(res_minz)
    cp_c = cross_over.calculateCp(df_for_cross_over)

    cp_c = [item[0] for item in cp_c]
    new_individuals = re_individual.select(cp = cp_c, old_individuals = individuals)
    
    df_of_new_individuals: [pd.DataFrame] = []

    for individual_position in range(0, len(new_individuals)):
        df_of_new_individual = read_data.convertIndividualToDataFrameForCriticalPath(individual = new_individuals[individual_position])
        df_of_new_individuals.append(df_of_new_individual)

    df_of_new_individuals_dict = convertIndividualsToDict(df_of_new_individuals)
   
    df_of_new_individuals_for_cross_over = perform_cross_over(df_of_new_individuals_dict)
    
    df_of_new_individuals_for_mutation = perform_mutation(df_of_new_individuals_for_cross_over)
    
    replaced_individuals = getReplacedIndividuals(df_of_new_individuals_dict, df_of_new_individuals_for_cross_over)
    replaced_individuals = getReplacedIndividuals(replaced_individuals, df_of_new_individuals_for_mutation)
    
    random_individuals: [Individual] = []
    if(len(savedAllIndividuals) >= 2): 
        random_individuals = random.choices(savedAllIndividuals, k = 2)
  
    return read_data.convertDataFrameToIndividuals(replaced_individuals, individuals= new_individuals, random_individuals = random_individuals)
    
    # print(df_of_new_individuals_for_mutation)
### Main programming
if __name__ == '__main__':
    log_duration = []
        
    numberOfDesiredRound: int = N_ROUNDS
    numberOfPerformingRound: int = 0

    individuals: [Individual] = None
    global savedAllIndividuals
    savedAllIndividuals: [Individual] = []

    
    while(numberOfPerformingRound < numberOfDesiredRound):
        print('--------------- perform round ' + str(numberOfPerformingRound))
        start_date_str = datetime.datetime.strftime(datetime.datetime.today(), '%d/%m/%Y-%H:%M:%S')

        if individuals is None:
            individuals: [Individual] = performIntializationPopulation()
        individuals = performRound(individuals= individuals, index_round=numberOfPerformingRound + 1)
        end_date_str = datetime.datetime.strftime(datetime.datetime.today(), '%d/%m/%Y-%H:%M:%S')
        
        start_date = datetime.datetime.strptime(start_date_str, '%d/%m/%Y-%H:%M:%S')
        end_date = datetime.datetime.strptime(end_date_str, '%d/%m/%Y-%H:%M:%S')

        print(end_date - start_date)
        log_duration_item = ['Round ' + str(numberOfPerformingRound), str(end_date - start_date)]
        log_duration.append(log_duration_item)
        numberOfPerformingRound += 1

    col_name_log_duration = ['Round Name', 'Duration of completed round']
    df_log_duration = pd.DataFrame(log_duration, columns = col_name_log_duration)
    df_log_duration.to_excel('log_duration.xlsx', index = False)

    # print(savedInitIndividual)
        