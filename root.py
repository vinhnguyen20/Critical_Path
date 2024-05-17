from typing import Any
import pandas as pd
import PySimpleGUI as pg

from collections import deque


nDesiredIndividual = 2
MAXN = 1000000

class Activity(): 
    def __init__(self, activity_number: int, predecessors: [], values: {}):
        self.activity_number = activity_number
        self.predecessors = predecessors

        # next activity save the number of activity,no mean save address activity
        self.pre_activities: [int] = predecessors
        self.next_activities: [int] = []
        self.values = values 

    def insert_next_activity(self, activity_number):
        self.next_activities.append(activity_number)

    def insert_prev_activity(self, activity_number):
        self.pre_activities.append(activity_number)

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
    
activity_manager = ActivityManager()
    
def CallbackItemOfActivity(index: int, row): 
    values = {}
    activity_number = row['Activity']
    predecessors = row['Predecessor']
    values['duration'] = row['Duration_of_normal_model']
    values['ES'] = 0
    values['EF'] = 0
    values['LF'] = MAXN
    values['LS'] = 0
    if predecessors == '-':
        predecessors = []
    else: 
        predecessors = [int(item) for item in str(predecessors).split(',')]
    
    newActivity = Activity(activity_number= activity_number, predecessors= predecessors, values= values)

    # Add the new activity  in Activity Management
    activity_manager.insert_activity(newActivity)
    for predecessor in predecessors:
        activity_manager.find_activity(predecessor).insert_next_activity(activity_number=activity_number)

    return newActivity

def ConvertDataToEntity(data, callbackItem: None): 
    res = []
    if(callbackItem is None): 
        raise ValueError("Please provide a callback")
     
    for index, row in data.iterrows():
        item: Activity = callbackItem(index, row)
        res.append(item)
    return res


def traceCriticalPath():
    activityItem: Activity = activity_manager.find_activity(activity_manager.end_activity)
    critical_paths = []
    while(len(activityItem.pre_activities) != 0):
        critical_paths.append(activityItem.activity_number)
        preActivities = activityItem.pre_activities
        maxPreActivitiesItem = None 
        for preActivity in preActivities: 
            subActivityItem = activity_manager.find_activity(activity_number=preActivity)
            LF = subActivityItem.values['LF']
            EF = subActivityItem.values['EF']
            if(LF == EF):
                maxPreActivitiesItem = preActivity

        if(maxPreActivitiesItem is None):
            raise ValueError("Please check data")
        
        for activity_number in preActivities:
            subActivityItem: Activity= activity_manager.find_activity(activity_number=activity_number)
            LF = subActivityItem.values['LF']
            EF = subActivityItem.values['EF']
            LF_of_maxEndActivity: int = activity_manager.find_activity(activity_number=maxPreActivitiesItem).values['LF']
            if(LF_of_maxEndActivity <= LF and LF == EF):
                activityItem = subActivityItem 
                
                
    return critical_paths
            
    
def calculateCriticicalPath(): 
    d_activities = deque()
    start_activity = activity_manager.get_start_activity()
    d_activities.append(start_activity)
    # calculate  ES and EF
    while(len(d_activities) != 0):
        cur_activity = d_activities.popleft()

        next_activities = cur_activity.next_activities
        for activity_number in next_activities:
            activity_item =  activity_manager.find_activity(activity_number=activity_number)
            d_activities.append(activity_item)

            # update the earliest start of the next activity 
            EF_of_cur_activity = cur_activity.values['EF']
            ES_of_nxt_activity = activity_item.values['ES'] 
            if(EF_of_cur_activity > ES_of_nxt_activity):
                activity_item.values['ES'] = EF_of_cur_activity

            # update the earliest finish of the next activity
            activity_item.values['EF'] = activity_item.values['ES'] + activity_item.values['duration']

    # calcualte LF and LS
    d_activities.clear()
    end_activity_numbers = activity_manager.save_end_activities
    for activity_number  in end_activity_numbers:
        activity_item = activity_manager.find_activity(activity_number=activity_number)        
        activity_item.values['LF'] = activity_item.values['EF']
        activity_item.values['LS'] = activity_item.values['LF'] - activity_item.values['duration']
        d_activities.append(activity_item)

    
    while(len(d_activities) != 0):

        cur_activity = d_activities.popleft()
        next_activities = cur_activity.pre_activities

        if(len(next_activities) == 0):
            activity_manager.save_end_activities.append(cur_activity.activity_number)

        for activity_number in next_activities:
            activity_item =  activity_manager.find_activity(activity_number=activity_number)
            d_activities.append(activity_item)

            LS_of_cur_activity = cur_activity.values['LS']
            LF_of_prev_activity = activity_item.values['LF']

            if(LS_of_cur_activity < LF_of_prev_activity):
                activity_item.values['LF'] = LS_of_cur_activity

            activity_item.values['LS'] = activity_item.values['LF'] - activity_item.values['duration']

    # Find the end of the activity that represents the maximum critical path
    
    endActivities = activity_manager.save_end_activities
    endActivitiesSize = len(endActivities)
    if(endActivitiesSize < 1):
        raise ValueError('Please check data')

    maxEndActivity = endActivities[0] 
    for endActivity in endActivities:
        activityItem = activity_manager.find_activity(endActivity)
        LF = activityItem.values['LF']
        LF_of_maxEndActivity = activity_manager.find_activity(maxEndActivity).values['LF']
        if(LF > LF_of_maxEndActivity):
            maxEndActivity = endActivity
    activity_manager.end_activity = maxEndActivity

        
def printDebugActivities():
    for activity_number in activity_manager.activities_manager.keys():
        activity: Activity = activity_manager.find_activity(activity_number)
        print('-----------------------')
        print('Activity Number: ' +  str(activity.activity_number))
        # print('List the Previous Activity : ' + str(activity.pre_activities)) 
        # print('List the Next Activity : ' + str(activity.next_activities)) 
        print(activity.values)



# Using DataFrame to read file excel


 
if __name__ == "__main__":
    nDesiredIndividual = 20
    for index in range(nDesiredIndividual):
        PREFIX_FILE_NAME_IN = "INDIVIDUAL_"
        SUFFIX_FILE_NAME_IN = index + 1
        file_name_in = PREFIX_FILE_NAME_IN + str(SUFFIX_FILE_NAME_IN)
        path_df = PREFIX_FILE_NAME_IN + str(SUFFIX_FILE_NAME_IN) + '.xlsx'
        df = pd.read_excel(path_df)

        
        activities: [Activity] = ConvertDataToEntity(df, callbackItem= CallbackItemOfActivity)

        # activities.__init__()

        activity_manager.run()

        # activity_manager.__init__()

        calculateCriticicalPath()
        # printDebugActivities()
        paths = traceCriticalPath()
        
        critical_paths = []
        activity_path = []
        for activity_number in paths:
            activityItem = activity_manager.find_activity(activity_number=activity_number)
            activity_number = activityItem.activity_number
            ES = activityItem.values['ES']
            EF = activityItem.values['EF']
            LS = activityItem.values['LS']
            LF = activityItem.values['LF']
            # critical_paths.append([activity_number, ES, EF, LS, LF])
            activity_path.append([activity_number])
        activities.__init__()
        activity_manager.__init__()


    #--------------------------------------extract file to calculate min Z-----------------------------------
        activity_path.reverse()

        activity_file = pd.DataFrame(activity_path)
        print(activity_path)

        activity_file.columns =['Activity']

        file_data = pd.DataFrame(df)

        # print(file_data)


        res_file = activity_file.merge(file_data, how = 'inner', on = ['Activity'])


        res_file['C_ij'] = (res_file['Cost_of_min_model'] - res_file['Cost_of_normal_model']) / (res_file['Duration_of_normal_model'] - res_file['Duration_of_min_model']) 

        res_file = res_file.fillna(0)

        res_file = res_file[['Activity','Duration_of_normal_model','Duration_of_min_model','C_ij']]

        res_file.rename(columns = {'test':'TEST', 'Duration_of_normal_model': 'Max_S', 'Duration_of_min_model': 'Min_S'}, inplace = True) 

        count = 1
        PREFIX_FILE_NAME_OUT = "FILE_MIN_Z_"
        SUFFIX_FILE_NAME_OUT = index + 1
        file_name_out = PREFIX_FILE_NAME_OUT + str(SUFFIX_FILE_NAME_OUT) + '.xlsx'
        res_file.to_excel(file_name_out,  index=False)
        
        # print(tam)
        print(res_file)



