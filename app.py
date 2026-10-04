from flask import Flask, render_template
import pandas as pd
import boto3
import os

app = Flask(__name__)

S3_BUCKET = "renuka-case-monitoring-data-2026-226147735303-us-east-1-an"
S3_FILE = "cases.xlsx"
LOCAL_FILE = "/tmp/cases.xlsx"


def load_cases():

    s3 = boto3.client("s3")

    s3.download_file(
        S3_BUCKET,
        S3_FILE,
        LOCAL_FILE
    )

    df = pd.read_excel(LOCAL_FILE)

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