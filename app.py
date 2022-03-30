from flask import Flask, render_template, redirect, url_for

import tasks


app = Flask(__name__)

tm = tasks.TasksModel()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html', all_table=tm.getAllTable(), due_table=tm.getDueTable(),
                           pri_table=tm.getPriTable(), cal=tasks.getcalendar())


@app.route('/completed', methods=['GET', 'POST'])
def completed():
    return render_template('completed.html', comp_table=tm.getCompTable())


@app.route('/due', methods=['GET', 'POST'])
def due():
    return render_template('due.html', due_table=tm.getDueTable())



