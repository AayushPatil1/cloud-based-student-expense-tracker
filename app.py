
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for expenses; we'll connect RDS later.
expenses = []

@app.route("/")
def home():
    total = sum(expense["amount"] for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )

@app.route("/add", methods=["POST"])
def add_expense():
    try:
        amount = float(request.form["amount"])

        if amount <= 0:
            return redirect(url_for("home"))

        category = request.form["category"]
        description = request.form["description"]

        expenses.append({
            "amount": amount,
            "category": category,
            "description": description
        })

    except (ValueError, KeyError):
        pass

    return redirect(url_for("home"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
