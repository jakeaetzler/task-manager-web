#
# task-manager-web: tasks.py
# Author: Jake Etzler
# Wrapper file for all backend operations on tasks
#

import checkvist
from flask_table import Table, Col
import datetime
import secret
import calendar

# Must put your own information in these fields if you want to run it yourself
USER = secret.USER
SECRET = secret.SECRET


#
# --Section for file classes--
#

#
# TaskTable: Class for generating flask-table of tasks
#
class TaskTable(Table):
    name = Col('Name')
    due = Col('Due')


#
# PriTaskTable: Class for generating flask-table of tasks ordered by priority with time column
#
class PriTaskTable(Table):
    name = Col('Name')
    due = Col('Due')
    time = Col('Time')


#
# Task: Object for parsing out information from task dictionary
#
class Task:
    def __init__(self, task):
        self.task = task
        self.name = str(task['content'][3:])
        self.due = str(task['due'])
        self.tdict = dict(name=self.name, due=self.due)
        self.status = str(task['status'])
        self.tags = task['tags_as_text']
        self.duedate = self.getDueDate()
        self.time = self.getTime()

    # Get date from tags
    def getDueDate(self):
        date = datetime.date(int(self.task['due'][:4]), int(self.task['due'][5:7]), int(self.task['due'][8:]))
        return date

    # Get time from tags
    def getTime(self):
        for i in range(len(self.tags)):
            if self.tags[i] == 't':
                return int(self.tags[i + 1])
        return 0


#
# TasksModel: Wrapper class for producing usable objects from API returned objects
#
class TasksModel:
    # Initialize the model
    def __init__(self):
        self.cl = getclient()
        self.tasks = self.getTasks()

    # Get all TaskManager tasks
    def getTasks(self):
        myTasks = self.cl.get_lists()
        tmid = str(myTasks['name' == 'TaskManager']['id'])
        tasks = self.cl.get_tasks(tmid)
        return tasks

    # Get html Flask table for all tasks
    def getAllTable(self):
        items = []
        for t in self.tasks:
            temp = Task(t)
            items.append(temp.tdict)
        table = TaskTable(items)
        return table

    # Get completed tasks
    def getCompTable(self):
        items = []
        for t in self.tasks:
            temp = Task(t)
            if temp.status == '1':
                items.append(temp.tdict)
        table = TaskTable(items)
        return table

    # Get list of due dates as Date comparable object
    # TODO: Obsolete with updates Task class attributes
    def getDueDates(self):
        dates = []
        for t in self.tasks:
            date = datetime.date(int(t['due'][:4]), int(t['due'][5:7]), int(t['due'][8:]))
            dates.append((t['content'][3:], date))
        return dates

    # Get due tasks
    def getDueTable(self):
        items = []
        for t in self.tasks:
            temp = Task(t)
            if temp.status == '0':
                items.append(temp.tdict)
        table = TaskTable(items)
        return table

    # Get list of tasks ordered by priority
    def getPriTasks(self):
        items = []
        for t in self.tasks:
            items.append(Task(t))
        # Use lambda functions to sort by time in reverse order, then by date
        pri_items = sorted(sorted(items, key=lambda x: x.time, reverse=True), key=lambda x: x.duedate)

        pri_list = []
        for t in pri_items:
            pri_list.append(t.task)
        return pri_list

    # Get prioritized task table\
    def getPriTable(self):
        items = []
        for t in self.getPriTasks():
            temp = Task(t)
            if temp.status == '0' and temp.duedate <= (datetime.date.today() + datetime.timedelta(days=5)):
                pdict = dict(name=temp.name, due=temp.due, time=str(temp.time))
                items.append(pdict)
        table = PriTaskTable(items)
        return table


#
# --Section for file functions--
#

# Retrieve API client
def getclient():
    cl = checkvist.user_account(USER, SECRET)
    cl.send_auth()
    user = cl.get_user()
    print(user['username'])
    return cl

# Generate HTML calendar for specified month
# TODO: Make automatically get days with due tasks
def getcalendar():
    cal = calendar.HTMLCalendar(firstweekday=0)
    month, yr = datetime.date.today().month.real, 2022
    return cal.formatmonth(yr, month)


#
# --Main for testing--
#

if __name__ == '__main__':
    tm = TasksModel()
    tasks = tm.getTasks()
    for t in tm.getPriTasks():
        print(t['content'])
        print(t['due'])
        print(t['tags_as_text'])

    print(tm.getPriTable())
