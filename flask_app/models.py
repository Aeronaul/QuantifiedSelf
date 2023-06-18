from sqlalchemy import Column, ForeignKey, asc, desc
from sqlalchemy.orm import Session

from flask_app import db, Base, engine

class Account(Base):
    __tablename__ = "accounts"
    username = Column(db.Text(), primary_key = True)
    password = Column(db.Text(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

def username_exists(username):
    with Session(engine) as session:
        matches = session.query(Account).filter_by(username=username).first()
        # print(matches)
        return matches is not None

def account_exists(username, password):
    with Session(engine) as session:
        matches = session.query(Account).filter_by(username=username, password=password).first()
        # print(matches)
        return matches is not None

def query(username, password):
    with Session(engine) as session:
        matches = session.query(Account).filter_by(username=username, password=password).first()
        # print(matches)
        return matches

def add_user(username, password):
    if not username_exists(username):
        with Session(engine) as session:
            account = Account(username, password)
            session.add(account)
            session.commit()
            return True
    else: return False

def del_user(username):
    if not username_exists(username):
        with Session(engine) as session:
            session.delete(session.query(Account)
                           .filter(Account.username == username)
                           .all())
            return True
    else: return False

def get_acc_list():
    with Session(engine) as session:
        return session.query(Account).all()


class Tracker(Base):
    __tablename__ = "trackers"
    id = Column(db.Integer(), autoincrement=True, primary_key=True)
    user = Column(db.Text(), ForeignKey('accounts.username'), nullable=False)
    name = Column(db.Text(), nullable=False)
    last_tracked = Column(db.Text())
    t_type = Column(db.Integer(), nullable=False) # 1: integer, 2: yes/no, 3: MCQ
    option_list = Column(db.Text())
    description = Column(db.Text())


    def __init__(self, user, name, last_tracked, tracker_type, description, option_list):
        self.user = user
        self.name = name
        self.last_tracked = last_tracked
        self.t_type = tracker_type
        self.option_list = option_list
        self.description = description

def get_trackers_list(user):
    # return Tracker.query.all()
    with Session(engine) as session:
        return session.query(Tracker).filter_by(user=user).all()

def get_tracker(user, name):
    with Session(engine) as session:
        return session.query(Tracker).filter_by(user=user, name=name).first()

def get_tracker_from_id(id):
    with Session(engine) as session:
        return session.query(Tracker).filter_by(id=id).first()

def tracker_exists(user, name):
    with Session(engine) as session:
        matches = session.query(Tracker).filter_by(user=user, name=name).first()
        return matches is not None

def tracker_add(user, name, desc="", tracker_type=0,last_tracked="", t_options=""):
    if not tracker_exists(user, name):
        with Session(engine) as session:
            tracker = Tracker(user, name, last_tracked, tracker_type=tracker_type, description=desc, option_list=t_options)
            session.add(tracker)
            session.commit()
            # print("committed", tracker)
            return True
    else: return False

def tracker_edit(user, old_name, name, desc="", tracker_type=0,last_tracked="", t_options=""):
    with Session(engine) as session:
        tracker = session.query(Tracker).filter_by(user=user, name=old_name).first()
        # print(tracker.name, tracker.t_type, tracker.description, tracker.user)
        tracker.name = name
        tracker.description = desc
        tracker.t_type = tracker_type
        tracker.last_tracked = last_tracked
        tracker.option_list = t_options
        session.commit()
        # print(tracker.name, tracker.t_type, tracker.description, tracker.user)
        # print("updated", tracker)

def tracker_delete(user, name):
    with Session(engine) as session:
        session.query(Tracker).filter_by(user=user, name=name).delete()
        session.commit()

class Log(Base):
    __tablename__ = "logs2"
    log_id = Column(db.Integer(), autoincrement=True, primary_key=True)
    tracker_id = Column(db.Integer(), ForeignKey('trackers.id'), nullable=False)
    date = Column(db.Text(), nullable=False)
    time = Column(db.Text())
    value = Column(db.Text(), nullable=False)
    notes = Column(db.Text())

    def __init__(self, tracker_id, date, time, value, notes):
        self.tracker_id = tracker_id
        self.date = date
        self.time = time
        self.value = value
        self.notes = notes

def insert_log(log: Log):
    with Session(engine) as session:
        session.add(log)
        session.commit()
        # print("committed", log)

def m_edit_log(log_id, date, time, value, notes):
    with Session(engine) as session:
        log = session.query(Log).filter_by(log_id=log_id).first()
        log.date = date
        log.time = time
        log.value = value
        log.notes = notes
        session.add(log)
        session.commit()
        # print("edited", log)

def retrieve_logs(tracker_id, distinct=False, sorted=False):
    with Session(engine) as session:
        if not distinct:
            if sorted:
                return session.query(Log).filter_by(tracker_id=tracker_id).order_by(asc(Log.value)).all()
            else:
                return session.query(Log).filter_by(tracker_id=tracker_id).all()
        else:
            return session.query(Log).filter_by(tracker_id=tracker_id).distinct().order_by(asc(Log.date)).order_by(asc(Log.value))

def retrieve_log(log_id):
    with Session(engine) as session:
        return session.query(Log).filter_by(log_id=log_id).first()

def log_delete(id):
    with Session(engine) as session:
        session.query(Log).filter_by(log_id=id).delete()
        session.commit()

def log_graph(tracker_id):
    l = retrieve_logs(tracker_id, True)
    x = [z.date for z in l]
    y = [z.value for z in l]
    y = [float(z) if get_tracker_from_id(tracker_id).t_type == 1 else z for z in y]

    # y2 = [float(z) for z in y if z.replace('.', '', 1).isdigit()]
    # if len(y2) == len(y): y = y2

    # if get_tracker_from_id(tracker_id).t_type == 3: y.sort()

    # if x and y:
        # x, y = zip(*sorted(zip(x, y)))
    return x, y

def get_last_modified(tracker_id):
    l = retrieve_logs(tracker_id, True)
    with Session(engine) as session:
        lmt = session.query(Log).filter_by(tracker_id=tracker_id).order_by(desc(Log.date)).order_by(desc(Log.time)).first()
        if lmt is not None:
            return lmt.date + " " + lmt.time
        else:
            return str()