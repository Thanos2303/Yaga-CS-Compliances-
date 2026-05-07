from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

# =========================
# COMPLIANCES DATA
# =========================

compliances = [

    # Drafting
    {
        "id": 1,
        "name": "Board Meeting Draft",
        "event_date": "2026-05-01",
        "due_date": "2026-05-10",
        "status": "Pending",
        "type": "drafting"
    },

    # ROC - Annual
    {
        "id": 2,
        "name": "AOC-4 Filing",
        "event_date": "2026-09-01",
        "due_date": "",
        "status": "Pending",
        "type": "roc",
        "period": "annual"
    },

    {
        "id": 3,
        "name": "MGT-7 Filing",
        "event_date": "2026-09-01",
        "due_date": "",
        "status": "Pending",
        "type": "roc",
        "period": "annual"
    },

    {
        "id": 4,
        "name": "DPT-3 Filing",
        "event_date": "2026-03-31",
        "due_date": "2026-06-30",
        "status": "Pending",
        "type": "roc",
        "period": "annual"
    },

    # ROC - Quarterly
    {
        "id": 5,
        "name": "Quarterly Board Meeting",
        "event_date": "2026-06-01",
        "due_date": "2026-06-30",
        "status": "Pending",
        "type": "roc",
        "period": "quarterly"
    },

    # ROC - Half-Yearly
    {
        "id": 6,
        "name": "Half-Yearly Return",
        "event_date": "2026-09-01",
        "due_date": "2026-09-30",
        "status": "Pending",
        "type": "roc",
        "period": "half"
    },

    # ROC - Event Based
    {
        "id": 7,
        "name": "DIR-12 Filing",
        "event_date": "2026-05-15",
        "due_date": "2026-05-20",
        "status": "Pending",
        "type": "roc",
        "period": "event"
    }
]

# =========================
# AUTO DUE DATE CALCULATION
# =========================

def calculate_due_dates():

    for c in compliances:

        if c["type"] == "roc" and c.get("period") == "annual":

            if c["name"] == "AOC-4 Filing":

                agm = datetime.strptime(c["event_date"], "%Y-%m-%d")

                c["due_date"] = (
                    agm + timedelta(days=30)
                ).strftime("%Y-%m-%d")

            elif c["name"] == "MGT-7 Filing":

                agm = datetime.strptime(c["event_date"], "%Y-%m-%d")

                c["due_date"] = (
                    agm + timedelta(days=60)
                ).strftime("%Y-%m-%d")

# =========================
# HOME
# =========================

@app.route("/")
def index():

    calculate_due_dates()

    today = datetime.today().date()

    for c in compliances:

        due = datetime.strptime(
            c["due_date"],
            "%Y-%m-%d"
        ).date()

        if c["status"] != "Completed" and due < today:
            c["status"] = "Overdue"

    return render_template(
        "index.html",
        compliances=compliances
    )

# =========================
# MARK DONE
# =========================

@app.route("/update/<int:id>")
def update(id):

    for c in compliances:

        if c["id"] == id:
            c["status"] = "Completed"

    return redirect("/")

@app.route("/dpt3")
def dpt3_page():
    return render_template("dpt3.html")# =========================


@app.route("/add", methods=["POST"])
def add_compliance():

    new_id = len(compliances) + 1

    compliances.append({

        "id": new_id,
        "name": request.form["name"],
        "event_date": request.form["event_date"],
        "due_date": request.form["due_date"],
        "status": "Pending",
        "type": request.form["type"],
        "period": request.form["period"]

    })

    return redirect("/")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5001)