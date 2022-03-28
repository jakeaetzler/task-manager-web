from flask import Flask, render_template, redirect, url_for

import tasks
from tasks import *

app = Flask(__name__)

tm = tasks.TasksModel()

@app.route('/')
def hello_world():
    return render_template('index.html', all_table=tm.getAllTable(), due_table=tm.getDueTable(),
                           pri_table=tm.getPriTable())


@app.route('/completed', methods=['GET', 'POST'])
def completed():
    return render_template('completed.html', comp_table=tm.getCompTable())




