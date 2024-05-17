from typing import Any



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


class ActivityManager():
    def __init__(self):
        self.activities_manager = {}

        self.start_activity: int = None
        self.end_activity: int  = None
        self.save_end_activities =  []

    def find_activity(self, activity_number) -> Activity:
        return self.activities_manager.get(activity_number)

    def insert_activity(self, activity: Activity):
        self.activities_manager[activity.activity_number] = activity

    def run(self):
        save_start_activities = []
        save_end_activities = []

        # Find all activities that either have a previous activity or have an empty nex activity 
        for activity in self.activities_manager.values():
            if(len(activity.pre_activities) == 0):
                save_start_activities.append(activity.activity_number)

            if(len(activity.next_activities) == 0):
                self.save_end_activities.append(activity.activity_number)

        # If the number of previous  activities is more than 1, add the start activity 
        if(len(save_start_activities) != 0):
            root_activity = Activity(0, predecessors=[], values = {
                'duration': 0,
                'ES': 0,
                'EF': 0,
                'LF': 0, 
                'LS': 0
            })
            self.start_activity = 0
            self.activities_manager[root_activity.activity_number] = root_activity
            for activity_number in save_start_activities: 
                self.activities_manager.get(activity_number).insert_prev_activity(root_activity.activity_number)
                self.activities_manager.get(root_activity.activity_number).insert_next_activity(activity_number)
        else:
            self.start_activity = save_start_activities[0]
        
    def get_start_activity(self):
        return self.activities_manager.get(self.start_activity)

    def get_end_activity(self):
        return self.activities_manager.get(self.end_activity)