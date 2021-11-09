
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session , url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":


        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        if day and month and not name:
            return render_template("error.html", message="Missing name, please enter THE name")
        elif name and day and not month:
            return render_template("error.html", message="Missing month, please enter THE month")
        elif month and name and not day:
            return render_template("error.html", message="Missing date, please enter THE date")

        elif not day or not  month or not name:
            return render_template("error.html", message="Missing data,look carefully")

        else:
            db.execute("INSERT INTO birthdays (name,day,month) VALUES(?, ?, ? )", name,day,month,)
            return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthday= db.execute("SELECT *FROM birthdays ")
        return render_template("index.html", birthday=birthday)



@app.route('/delete/<string:name>', methods = ['GET'])
def delete(name):
    db.execute("DELETE FROM birthdays WHERE name=%s", (name))
    return redirect(url_for("index"))


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    people= db.execute("select * from birthdays where id=id")
    if request.method == 'PUT':
        people.name = request.form.get("name")
        people.day = request.form.get("day")
        people.month = request.form.get("month")
        db.session.commit()
        return redirect("/index")
    else:
         return render_template("update.html", people=people )


