from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxut37m54in4HoFdE4abKAcfir0Dh2LLxPHc-N0WW_aousZa5f6CqaaGvulJu64WZtf/exec"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():

    # Get form data
    company_name = request.form.get("company_name")
    contact_person = request.form.get("contact_person")
    pickup = request.form.get("pickup")
    delivery = request.form.get("delivery")
    goods = request.form.get("goods")
    truck_type = request.form.get("truck_type")
    weight = request.form.get("weight")
    message = request.form.get("message")

    required_date = request.form.get("required_date")

    # Convert YYYY-MM-DD to DD-MM-YYYY
    if required_date:
        try:
            required_date = datetime.strptime(
                required_date,
                "%Y-%m-%d"
            ).strftime("%d-%m-%Y")

        except ValueError:
            pass

    # Data to send to Google Apps Script
    booking_data = {
        "company_name": company_name,
        "contact_person": contact_person,
        "pickup": pickup,
        "delivery": delivery,
        "goods": goods,
        "truck_type": truck_type,
        "weight": weight,
        "required_date": required_date,
        "message": message
    }

    # Print enquiry in terminal
    print("\n========== NEW TRUCK ENQUIRY ==========")
    print("Company Name:", company_name)
    print("Contact Number:", contact_person)
    print("Pickup Location:", pickup)
    print("Delivery Location:", delivery)
    print("Goods:", goods)
    print("Truck Type:", truck_type)
    print("Approx Weight:", weight)
    print("Required Date:", required_date)
    print("Message:", message)
    print("=======================================\n")

    # Send enquiry to Google Apps Script
    try:

        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=booking_data,
            timeout=8
        )

        print("Google Script Status:", response.status_code)
        print("Google Script Response:", response.text)

        # Google Sheet successfully received data
        if response.ok:

            return jsonify({
                "success": True,
                "message": "Your truck request has been submitted successfully."
            })

        # Google Script returned an error
        return jsonify({
            "success": False,
            "message": "Unable to submit your request. Please try again."
        }), 500

    except requests.exceptions.Timeout:

        print("Google Script Error: Request timed out")

        return jsonify({
            "success": False,
            "message": "Request is taking too long. Please try again."
        }), 504

    except requests.exceptions.RequestException as error:

        print("Google Script Error:", error)

        return jsonify({
            "success": False,
            "message": "Unable to submit your request. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)