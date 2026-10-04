from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


def load_cases():
    df = pd.read_excel("cases.xlsx")

    cases = []

    for _, row in df.iterrows():
        cases.append({
            "case": str(row["Case Number"]),
            "priority": str(row["Priority"]),
            "status": str(row["Status"]),
            "escalated": str(row["Escalated"]),
            "acknowledged": str(row["Acknowledged"]),
            "followup": str(row["Next followp date & time"])
        })

    return cases


@app.route("/")
def dashboard():

    cases = load_cases()

    total = len(cases)

    open_cases = sum(
        1 for case in cases
        if case["status"] == "Open"
    )

    resolved_cases = sum(
        1 for case in cases
        if case["status"] == "Resolved"
    )

    escalated_cases = sum(
        1 for case in cases
        if case["escalated"] == "Yes"
    )

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