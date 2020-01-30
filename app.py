from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PowerMax300@localhost/happiness_collector'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mzpsznnyzixnsk:cdaea47157753142b0aef7a039b2573fbfc439f6d58f9d62c469670ec95cff14@ec2-52-71-122-102.compute-1.amazonaws.com:5432/dc60a0srbajg2u?sslmode=require'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    happiness_ = db.Column(db.Integer)
    age_ = db.Column(db.String(20))

    def __init__(self, email_, happiness_, age_):
        self.email_ = email_
        self.age_ = age_
        self.happiness_ = happiness_


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':

        # extract user input
        age = request.form.get('age_name')
        level = request.form.get('level_name')
        email = request.form["email_name"]

        # add rows to data base if email is unique
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, level, age)
            db.session.add(data)
            db.session.commit()

            # happiest age group
            happiest_age = find_happiest_age()

            # average level of happiness
            avg_happiness = round(db.session.query(
                func.avg(Data.happiness_)).scalar(), 1)

            # is the user happier than average
            is_happier = "happier" if float(
                level) > avg_happiness else "less happy"

            # how many people participated so far
            total_participants = db.session.query(Data).count()

            send_email(email, level, age, avg_happiness,
                       is_happier, total_participants, happiest_age)
            return render_template("result.html")
    return render_template('index.html',
                           text="Seems like we've got something from that email address already!")


def find_happiest_age():
    if db.session.query(Data).filter(Data.age_ == "childhood").count() != 0:
        age_childhood = round(db.session.query(
            func.avg(Data.happiness_).filter(Data.age_ == "childhood")).scalar(), 1)
    else:
        age_childhood = 0

    if db.session.query(Data).filter(Data.age_ == "youth").count() != 0:
        age_youth = round(db.session.query(
            func.avg(Data.happiness_).filter(Data.age_ == "youth")).scalar(), 1)
    else:
        age_youth = 0

    if db.session.query(Data).filter(Data.age_ == "adulthood").count() != 0:
        age_adulthood = round(db.session.query(
            func.avg(Data.happiness_).filter(Data.age_ == "adulthood")).scalar(), 1)
    else:
        age_adulthood = 0

    if db.session.query(Data).filter(Data.age_ == "seniority").count() != 0:
        age_seniority = round(db.session.query(
            func.avg(Data.happiness_).filter(Data.age_ == "seniority")).scalar(), 1)
    else:
        age_seniority = 0

    age_level_happiness = {"childhood": age_childhood, "youth": age_youth,
                           "adulthood": age_adulthood, "seniority": age_seniority}
    return max(age_level_happiness, key=age_level_happiness.get)


if __name__ == '__main__':
    app.debug = True
    app.run()
