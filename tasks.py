from abc import ABC

import checkvist
from flask_table import Table, Col

USER = 'jboss224@gmail.com'
SECRET = '9SXUhi42q1EzyI'


#
# --Section for file classes--
#


class TaskTable(Table):
    name = Col('Name')
    due = Col('Due')


class Task:
    def __init__(self, task):
        self.name = str(task['content'][3:])
        self.due = str(task['due'])
        self.tdict = dict(name=self.name, due=self.due)
        self.status = str(task['status'])

class TasksModel:
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

    # Get due tasks
    def getDueTable(self):
        items = []
        for t in self.tasks:
            temp = Task(t)
            if temp.status == '0':
                items.append(temp.tdict)
        table = TaskTable(items)
        return table


#
# --Section for file functions--
#

def getclient():
    cl = checkvist.user_account(USER, SECRET)
    cl.send_auth()
    user = cl.get_user()
    print(user['username'])
    return cl



