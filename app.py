from flask import Flask, render_template, redirect, url_for, request

import tasks

app = Flask(__name__)

tm = tasks.TasksModel()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # Code for API refresh button function
    # TODO: extract this function (maybe)
    form = request.form
    if request.method == 'POST':
        if form.get('refresh-api') == 'Refresh Tasks':
            tm.refresh()
    elif request.method == 'GET':
        return render_template('index.html', form=form, all_table=tm.getAllTable(), due_table=tm.getDueTable(),
                               pri_table=tm.getPriTable(), cal=tasks.getcalendar(), overdue_table=tm.getOverdueTable())

    return render_template('index.html', form=form, all_table=tm.getAllTable(), due_table=tm.getDueTable(),
                           pri_table=tm.getPriTable(), cal=tasks.getcalendar(), overdue_table=tm.getOverdueTable())


@app.route('/completed', methods=['GET', 'POST'])
def completed():
    return render_template('completed.html', comp_table=tm.getCompTable())


@app.route('/due', methods=['GET', 'POST'])
def due():
    return render_template('due.html', due_table=tm.getDueTable())
