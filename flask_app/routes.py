from flask import render_template, request, redirect, url_for, flash

from flask_app import app
from flask_app.models import username_exists, account_exists, add_user, tracker_exists, get_trackers_list, \
    get_tracker, tracker_edit, tracker_add, tracker_delete, Log, insert_log, retrieve_logs, retrieve_log, m_edit_log, \
    get_tracker_from_id, log_delete, log_graph

import datetime
import matplotlib.pyplot as plt

CURRENT_USER = None


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        global CURRENT_USER
        u = request.form['username']
        p = request.form['password']
        if len(u) == 0 or len(p) == 0:
            flash("Fill all the fields!", category="danger")
        elif not username_exists(u):
            flash("Username does not exist!", category="danger")
        elif not account_exists(u, p):
            flash("Wrong password!", category="danger")
        else: CURRENT_USER = u
    if CURRENT_USER is not None:
        return redirect(url_for('dashboard', user=CURRENT_USER))
    return render_template('login.html', logged_in=False)


@app.route('/logout')
def logout():
    global CURRENT_USER
    CURRENT_USER = None
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p1 = request.form['password']
        p2 = request.form['c_password']
        if len(u) == 0 or len(p1) == 0 or len(p2) == 0:
            flash("Fill all the fields!", category="danger")
            return redirect(url_for('register'))
        elif p1 != p2:
            flash("Passwords do not match!", category="danger")
            return redirect(url_for('register'))
        elif username_exists(u):
            flash("Username already exists!", category="danger")
            return redirect(url_for('register'))
        else:
            add_user(u, p1)
            flash("Account created successfully! You can now login in.", category="success")
            return redirect(url_for('login'))
    return render_template('register.html', logged_in=False)


@app.route(f'/user/<user>', methods=['POST', 'GET'])
def dashboard(user):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    tracker_entries = get_trackers_list(user)
    # print(tracker_entries)
    return render_template('dashboard.html', logged_in=True, username=user, tracker_entries=tracker_entries)


@app.route('/track/<t_activity>')
def tracker(t_activity):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    g_tracker = get_tracker(CURRENT_USER, t_activity)
    logs = retrieve_logs(g_tracker.id, sorted=True)
    logs2 = retrieve_logs(g_tracker.id, sorted=False)
    x,y = log_graph(g_tracker.id)

    plt.plot(x, y, color='r')
    plt.xlabel("Date (yyyy-mm-dd)")
    plt.ylabel(g_tracker.name)
    if len(set(x)) > 5:
        plt.xticks(range(len(set(x))), sorted(list(set(x))), rotation=90)
    plt.savefig(f"flask_app/static/{CURRENT_USER}_{g_tracker.name}.png", bbox_inches='tight')
    plt.close()

    plt.show()


    return render_template('tracker.html', logged_in=True, username=CURRENT_USER, activity=t_activity, graph_img=(CURRENT_USER or '') + '_' + t_activity+'.png', log_entries=logs2)

@app.route('/track/<t_activity>/log', methods=['POST', 'GET'])
def logger(t_activity):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    t = get_tracker(CURRENT_USER, t_activity)

    if request.method == 'POST':
        time = request.form['time']
        date = request.form['date']
        value = request.form['value']
        notes = request.form['notes']

        if len(date) == 0:
            flash("You must specify a date!")
            return redirect(url_for('logger', t_activity=t_activity))

        if len(value) == 0:
            flash("You must specify a value!")
            return redirect(url_for('logger', t_activity=t_activity))

        log = Log(t.id, date, time, value, notes)
        insert_log(log)
        return redirect(url_for('tracker', t_activity=t.name))

    t_options = [z.strip() for z in t.option_list.split(',') if len(z.strip()) > 0]
    now = datetime.datetime.now()
    curr_date = now.strftime("%Y-%m-%d")
    curr_time = now.strftime("%H:%M")
    return render_template('log_add.html', logged_in=True, username=CURRENT_USER, activity=t_activity, tracker_type=t.t_type, tracker_options=t_options, curr_date=curr_date, curr_time=curr_time)

@app.route('/log-edit/<id>', methods=['POST', 'GET'])
def edit_log(id):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    log = retrieve_log(id)
    t = get_tracker_from_id(log.tracker_id)
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        value = request.form['value']
        notes = request.form['notes']
        if len(date) == 0:
            flash("You must specify date!")
            return redirect(url_for('edit_log', id=id))
        m_edit_log(log.log_id, date, time, value, notes)
        return redirect(url_for('tracker', t_activity=t.name))

    t_options = [z.strip() for z in t.option_list.split(',') if len(z.strip()) > 0]
    return render_template('log_edit.html', username=CURRENT_USER, id=id, tracker_type=t.t_type, tracker_options=t_options, activity=t.name, v_date=log.date, v_time=log.time, v_val=log.value, v_notes=log.notes)

@app.route('/log-del/<id>')
def delete_log(id):
    if not CURRENT_USER:
        return redirect(url_for('logout'))
    log = retrieve_log(id)
    t = get_tracker_from_id(log.tracker_id)
    log_delete(id)
    return redirect(url_for('tracker', t_activity=t.name))

@app.route('/tracker-add', methods=['POST', 'GET'])
def add_tracker():
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    if request.method=='POST':
        name = request.form['tracker_name']
        desc = request.form['tracker_desc']
        t_type = request.form['tracker_type']
        type_no = 0
        # print(t_type)
        t_options = ""
        if t_type == "Numeric":
            type_no = 1
        if t_type == "Yes/No":
            type_no = 2
        if t_type == "Multiple Choice":
            type_no = 3
            t_options = request.form['tracker_options']
        if len(name) == 0 or (t_type == "Multiple Choice" and len(t_options) == 0):
            flash("Fill all the fields!")
            return redirect(url_for('add_tracker'))
        if tracker_exists(CURRENT_USER, name):
            flash("Tracker already exists!")
            return redirect(url_for('add_tracker'))
        tracker_add(CURRENT_USER, name=name, tracker_type=type_no, desc=(desc or ""), t_options=(t_options or ""))
        return redirect(url_for('login'))

    if not CURRENT_USER:
        return redirect(url_for('logout'))
    return render_template('tracker_add.html', logged_in=True, username=CURRENT_USER)

@app.route('/tracker-edit/<name>', methods=['POST', 'GET'])
def edit_tracker(name):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    t = get_tracker(CURRENT_USER, name)

    if request.method == 'POST':
        name = request.form['tracker_name']
        desc = request.form['tracker_desc']
        t_type = request.form['tracker_type']
        type_no = 0
        # print(t_type)
        t_options = ""
        if t_type == "Numeric":
            type_no = 1
        if t_type == "Yes/No":
            type_no = 2
        if t_type == "Multiple Choice":
            type_no = 3
            t_options = request.form['tracker_options']
        if len(name) == 0 or (t_type == "Multiple Choice" and len(t_options) == 0):
            flash("Fill all the fields!")
            return redirect(url_for('edit_tracker', name=name))
        tracker_edit(CURRENT_USER, old_name=t.name, name=name, tracker_type=type_no, desc=(desc or ""), t_options=(t_options or ""))
        return redirect(url_for('login'))

    return render_template('tracker_edit.html', logged_in = True, username=CURRENT_USER, val_name=t.name, val_desc=t.description, val_type=t.t_type, val_options=t.option_list)


@app.route('/tracker-del/<name>')
def delete_tracker(name):
    if not CURRENT_USER:
        return redirect(url_for('logout'))

    tracker_delete(CURRENT_USER, name)
    return redirect(url_for('login'))