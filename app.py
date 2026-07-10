"""
app.py
------
Flask backend for the House Price Prediction project.

Routes:
    GET  /            -> Home page
    GET  /about        -> About page (explains the ML behind the project)
    GET  /prediction    -> Prediction form page
    POST /prediction    -> Runs the model and renders the result page
    GET  /contact       -> Contact page
    POST /contact       -> Handles the contact form (flash message)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

from model import get_model

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Load model once at startup so requests are fast
house_model = get_model()

LOCATIONS = house_model.meta["location_classes"]
CONDITIONS = house_model.meta["condition_classes"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", results=house_model.meta["results"],
                            best_model=house_model.meta["best_model_name"])


@app.route("/prediction", methods=["GET"])
def prediction_form():
    return render_template(
        "prediction.html", locations=LOCATIONS, conditions=CONDITIONS
    )


@app.route("/prediction", methods=["POST"])
def prediction_submit():
    try:
        result = house_model.predict(request.form)
    except (KeyError, ValueError) as exc:
        flash(f"Invalid input: {exc}. Please check the form and try again.")
        return redirect(url_for("prediction_form"))

    input_summary = {
        "Area (sq ft)": request.form.get("area"),
        "Bedrooms": request.form.get("bedrooms"),
        "Bathrooms": request.form.get("bathrooms"),
        "Floors": request.form.get("floors"),
        "Parking": request.form.get("parking"),
        "Year Built": request.form.get("year_built"),
        "Location": request.form.get("location"),
        "Condition": request.form.get("condition"),
        "Nearby Schools": request.form.get("schools"),
        "Nearby Hospitals": request.form.get("hospitals"),
        "Near Metro": "Yes" if request.form.get("metro") == "1" else "No",
    }

    return render_template("result.html", result=result, inputs=input_summary)


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/contact", methods=["POST"])
def contact_submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("All fields are required.")
        return redirect(url_for("contact"))

    # In a real project you'd store this in a DB or send an email.
    # Here we just acknowledge receipt.
    flash(f"Thanks {name}! Your message has been received.")
    return redirect(url_for("contact"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
