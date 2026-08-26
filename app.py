from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxut37m54in4HoFdE4abKAcfir0Dh2LLxPHc-N0WW_aousZa5f6CqaaGvulJu64WZtf/exec"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():

    company_name = request.form.get("company_name")
    contact_person = request.form.get("contact_person")
    pickup = request.form.get("pickup")
    delivery = request.form.get("delivery")
    goods = request.form.get("goods")
    truck_type = request.form.get("truck_type")
    required_date = request.form.get("required_date")
    weight = request.form.get("weight")
    message = request.form.get("message")

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

    # Print enquiry in VS Code terminal
    print("\n========== NEW TRUCK ENQUIRY ==========")
    print("Company Name:", company_name)
    print("Contact Person:", contact_person)
    print("Pickup Location:", pickup)
    print("Delivery Location:", delivery)
    print("Goods:", goods)
    print("Truck Type:", truck_type)
    print("Required Date:", required_date)
    print("Approx Weight:", weight)
    print("Message:", message)
    print("=======================================\n")

    # Send enquiry to Google Apps Script
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=booking_data,
            timeout=15
        )

        print("Google Script Status:", response.status_code)
        print("Google Script Response:", response.text)

    except requests.exceptions.RequestException as error:
        print("Google Script Error:", error)

    return render_template(
        "index.html",
        success=True,
        company_name=company_name
    )


if __name__ == "__main__":
    app.run(debug=True)