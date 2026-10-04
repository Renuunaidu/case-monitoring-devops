from flask import Flask, render_template

app = Flask(__name__)

cases = [
    {
        "case": "CS00111",
        "priority": "P1",
        "status": "Open",
        "escalated": "No",
        "acknowledged": "No",
        "followup": "04-10-2026 16:00"
    },
    {
        "case": "CS00112",
        "priority": "P1",
        "status": "Open",
        "escalated": "No",
        "acknowledged": "No",
        "followup": "04-10-2026 17:00"
    },
    {
        "case": "CS00113",
        "priority": "P2",
        "status": "Resolved",
        "escalated": "No",
        "acknowledged": "Yes",
        "followup": "RESOLVED"
    },
    {
        "case": "CS00114",
        "priority": "P3",
        "status": "Open",
        "escalated": "Yes",
        "acknowledged": "Yes",
        "followup": "05-10-2026 17:00"
    },
    {
        "case": "CS00115",
        "priority": "P2",
        "status": "Open",
        "escalated": "No",
        "acknowledged": "Yes",
        "followup": "05-10-2026 17:00"
    },
    {
        "case": "CS00116",
        "priority": "P3",
        "status": "Resolved",
        "escalated": "No",
        "acknowledged": "Yes",
        "followup": "RESOLVED"
    },
    {
        "case": "CS00117",
        "priority": "P1",
        "status": "Open",
        "escalated": "Yes",
        "acknowledged": "No",
        "followup": "04-10-2026 19:00"
    },
    {
        "case": "CS00118",
        "priority": "P3",
        "status": "Open",
        "escalated": "Yes",
        "acknowledged": "No",
        "followup": "04-10-2026 19:00"
    }
]


@app.route("/")
def dashboard():

    total = len(cases)
    open_cases = sum(1 for case in cases if case["status"] == "Open")
    resolved_cases = sum(1 for case in cases if case["status"] == "Resolved")
    escalated_cases = sum(1 for case in cases if case["escalated"] == "Yes")

    priority_counts = {
        "P1": sum(1 for case in cases if case["priority"] == "P1"),
        "P2": sum(1 for case in cases if case["priority"] == "P2"),
        "P3": sum(1 for case in cases if case["priority"] == "P3"),
        "P4": sum(1 for case in cases if case["priority"] == "P4")
    }

    critical_cases = [
        case for case in cases
        if case["escalated"] == "Yes"
        and case["acknowledged"] == "No"
    ]

    return render_template(
        "index.html",
        total=total,
        open_cases=open_cases,
        resolved_cases=resolved_cases,
        escalated_cases=escalated_cases,
        priority_counts=priority_counts,
        critical_cases=critical_cases,
        cases=cases
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)