from typing import Any
import pandas as pd

from collections import deque

from typing import Optional, Text, Dict, List, Union, Iterable, Any
import numpy as np
import random
from elistic import perform_elistic

nDesiredIndividual = 20



class Model():
    def __init__(self, model_number: int, values: {}):
        self.model_number = model_number
        self.values = values

class Activity():
    def __init__(self, activity_number: int, predecessor: [int], models: [Model]) -> None:
       self.activity_number = activity_number
       self.predecessor = predecessor
       self.models = models
       self.minModel = None

       self.pre_activities: [int] = predecessor
       self.next_activities: [int] = []

class Individual():
    def __init__(self):
        self.activities: [Any] = []
        self.models: [Model] = []
        self.minZ = None

    def addActivityWithChoicedModel(self, activity: Activity, model: Model):
        if(activity is None):
            raise ValueError("Activity is None")

        if model is None:
            raise ValueError("Please provide a choiced model")

        self.activities.append(activity)
        self.models.append(model)

class ActivityManager():
    def __init__(self):
        self.activity_manager = {}

    def CreateActivity(self, activity_number: int, predecessor: [int], models: [Model]) -> Activity:
        newActivity = Activity(activity_number = activity_number, predecessor = predecessor, models = models)
        self.activity_manager[activity_number] = newActivity
        return self.activity_manager[activity_number]

    def getActivity(self, activity_number) ->  Activity:
        return self.activity_manager[activity_number]

    def getAllActivities(self):
        data = []
        for activity in self.activity_manager.values():
            data.append(activity)
        return data

activity_manager = ActivityManager()

def format_data(df) -> [Activity]:
  new_data = df.iloc[1::, ::].copy()

  activities = []

  for index, value in new_data.iterrows():
      activity_number = value['Activity']
      predecessor = value['Predecessor']
      if(predecessor == '-'):
        predecessor =  []
      else:
        if(type(predecessor) == int):
          predecessor = [predecessor]
        else:
          predecessor = [ x for x in predecessor.split(',')]

      # Xử lý model của activity
      model_names = value[2::].index
      models = []
      modelSize = len(model_names)
      for i in range(0, modelSize, 2):
        costOfModel = value[model_names[i]]
        durationOfModel = value[model_names[i + 1]]
        if(costOfModel != '-' and durationOfModel != '-'):
          model = Model(model_number = (int(i/2) + 1), values = {
              'Cost': costOfModel,
              'Duration': durationOfModel
          })
          models.append(model)

      activity = activity_manager.CreateActivity(activity_number = int(activity_number), predecessor = predecessor, models = models)
      activities.append(activity)

  return activities



def GetMinDurationOfEachActivity(activity: Activity) -> Model:

    models: [Model] = activity.models
    modelSize = len(models)
    if(modelSize <= 0):
        return None
    else:
        res = models[0]
        for model in models:
            if(model.values['Duration'] < res.values['Duration']):
                res = model
        return res

def GetMinDurationOfActivities(activities: [Activity]) -> Activity:
    minModelOfActivity: Model = GetMinDurationOfEachActivity(activity=activities[0])
    minActivity = activities[0]
    for activity in activities:
        modelOfCurrentActivity: Model = GetMinDurationOfEachActivity(activity = activity)
        if(modelOfCurrentActivity is not None):
            minModelDuration = minModelOfActivity.values['Duration']
            currentModelDuration = modelOfCurrentActivity.values['Duration']
            if(minModelDuration > currentModelDuration):
                minModelOfActivity = modelOfCurrentActivity
                minActivity = activity
        else:
            print("Model of Activity is NULL")
    return minActivity


def setMinModelOfEachActivity(activities: [Activity]):
    for activity in activities:
        minModelOfActivity: Model = GetMinDurationOfEachActivity(activity= activity)
        activity.minModel = minModelOfActivity


def CreateDataset(nActivity):
    data = []
    for i in range(1, nActivity):
        # data.append(CreateActivity(i))
        activity_manager.CreateActivity(i)

    data = activity_manager.getAllActivities()
    return data

def CreateEachIndividual(activities: [Activity] = []) -> [Individual]:
    individual = Individual()
    for activity in activities:
        models = activity.models
        model = random.choice(models)
        # print(model.model_number)
        individual.addActivityWithChoicedModel(activity=activity, model=model)

    return individual

def CallbackOnlyModelNumberForEachActivity(model: Model):
    return {
        'model_number': model.model_number,
        'values': model.values}

def CallbackOnlyModelNumber(model: Model):
    return model.model_number

def InitPopulation(nDesiredIndividual: int = 30, activities: [Activity] = []) -> [Model]:
    activitiesSize = len(activities)
    if(activitiesSize == 0):
        raise ValueError("Please supply at least one Activity")

    if(nDesiredIndividual <= 0):
        raise ValueError("No existing the number of Population")

    nCreatedIndividualCount = 1
    individuals: [Individual] = []
    while(nCreatedIndividualCount <= nDesiredIndividual):
        individual = CreateEachIndividual(activities=activities)
        individuals.append(individual)
        activities = individual.activities
        models = individual.models
        nCreatedIndividualCount = nCreatedIndividualCount + 1

    return individuals


def printActivities(activities: [Activity]):
    for activity in activities:
        print('Activity ' + str(activity.activity_number) + ': \n')
        print(activity)
        print(activity.predecessor)
        models = activity.models
        for model in models:
            print(model.values)


"""
    Target: 
    - Convert an individual to a DataFrame in order to find the critical path
"""
def convertIndividualToDataFrameForCriticalPath(individual: Individual):
    activities = individual.activities
    models = individual.models
    size = len(activities)

    data = {
        'Activity': [], 
        'Predecessor': [], 
        'Duration_of_normal_model': [], 
        'Cost_of_normal_model': [],
        'Duration_of_min_model': [],
        'Cost_of_min_model': [],
        'Mode_number': [],
        'Number_of_mode': []
        }
    for pos in range(0, size, 1):
      activity = activities[pos]
      model = models[pos]
      
      activity_number = activity.activity_number
      predecessors = activity.predecessor
      time = model.values['Duration']
      
      if(len(predecessors) == 0):    predecessors = '-'
      else: predecessors = ', '.join(str(x) for x in predecessors)
      
      data['Activity'].append(activity_number)
      data['Predecessor'].append(predecessors)
      data['Duration_of_normal_model'].append(str(time))

      min_model = activity.minModel
      data['Cost_of_min_model'].append(min_model.values['Cost'])
      data['Cost_of_normal_model'].append(model.values['Cost'])
      data['Duration_of_min_model'].append(min_model.values['Duration'])

      #Number mode
      data['Mode_number'].append(model.model_number)
      data['Number_of_mode'].append(len(activity.models))

    marks_data = pd.DataFrame(data)
    return marks_data
    
def getModeNumberOfActivity(activity: Activity, desired_model_number):
    models = activity.models
    for model in models:
        model_number = model.model_number
        if model_number == desired_model_number:
            return model
    return models[0]

def printTheModelOfIndividual(individuals: [Individual]):
    for individual in individuals: 
        models = individual.models
        number_models = []
        for model in models:
            number_models.append(model.model_number)
        print(number_models)

      
def convertDataFrameToIndividuals(data: {}, individuals: [Individual] = None, random_individuals: [Individual] = None) -> [Individual]:
    newIndividuals: [Individual] = individuals.copy()
        
    if data is None or individuals is None: 
        raise ValueError('Please provide a data of both arguments')
    
    ### data provide the mode_numbers of the replaced individuals
    for key in data.keys():
        df_individual = data[key]
        individual = individuals[key]
        new_mode_numbers = df_individual['Mode_number'].to_numpy()
        print('Show all mode number', new_mode_numbers)
        print('Show all key', str(key))
        # print('-------------- Show individual after finishing round')
        models = individual.models

        activities = individual.activities
        for i in range(0, len(activities)):
            new_mode_number = new_mode_numbers[i]
            models[i] = getModeNumberOfActivity(activities[i], desired_model_number=new_mode_number)

    newIndividuals: [Individual] = perform_elistic(individuals=newIndividuals, random_individuals=random_individuals)

    return newIndividuals

def transferDataFrameToIndividual(data: {}) -> [Individual]:
    print(data)


def getAllActivities(df):
    activities = format_data(df)
    setMinModelOfEachActivity(activities = activities)
    return activities

def getAllIndividuals(nDesiredIndividual: int, activities: [Activity]):
    individuals: [Individual] = InitPopulation(nDesiredIndividual= nDesiredIndividual, activities= activities)
    return individuals


def extractIndividualToExcel(individuals: [Individual]):
    count = 1 
    PREFIX_FILE_NAME = "INDIVIDUAL_"
    SUFFIX_FILE_NAME = count
    for individual in individuals:
      file_name = PREFIX_FILE_NAME + str(SUFFIX_FILE_NAME) + '.xlsx'
      marks_data = convertIndividualToDataFrameForCriticalPath(individual)
      marks_data.to_excel(file_name,  index=False)
      count = count + 1
      SUFFIX_FILE_NAME = count

# if __name__ == "__main__":
#     # InitPopulation(nDesiredIndividual=nPopulation, activities=data)
#     # activities = CreateDataset(nActivity=5)


#     activities = getAllActivities(df)
#     individuals: [Individual] = getAllIndividuals(nDesiredIndividual=20, activities=activities)
    
#     extractIndividualToExcel(individuals)
    