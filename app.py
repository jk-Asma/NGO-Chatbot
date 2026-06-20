import google.generativeai as genai
import os
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
# for m in genai.list_models():
#     print(m.name)
# create model
model = genai.GenerativeModel("gemini-flash-latest")
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# creating database
def create_database():

    conn = sqlite3.connect("volunteers.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        hours TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        amount TEXT,
        cause TEXT
    )
    """)


    conn.commit()
    conn.close()


# global var to save user state and vol data
user_state ={}
volunteer_data={}
donation_data = {}

memory_store = []

#tell flask to load homepage

@app.route("/")
def home():
    return render_template("index.html")

  # receive msg and return response

# @app.route("/chat", methods=["POST"])
# def chat():
    # user_message = request.json.get("message","")

    # memory_store.append(user_message)

    # if "volunteer" in user_message.lower():
    #     reply = "I can help you register as a volunteer. Please share your skills and availability."
    # elif "donate" in user_message.lower():
    #     reply = "Thank you for your interest in donating. I can guide you through the donation process."
    # else:
    #     reply = "Hello! I am NayePankh AI Assistant. How can I help you today ?"

    # return jsonify({
    #     "reply": reply,
    #     "memory_count": len(memory_store)
    # })

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message", "")

    # donation workflow add
    if ("donate" or "donation")in user_message.lower():

        user_state["step"] = "donor_name"

        return jsonify({
            "reply":"Thank you for supporting NayePankh Foundation. What is your full name?"
    })
    if user_state.get("step") == "donor_name":

        donation_data["name"] = user_message

        user_state["step"] = "donor_email"

        return jsonify({
            "reply":"Please enter your email address."
    })

    if user_state.get("step") == "donor_email":

        donation_data["email"] = user_message

        user_state["step"] = "donor_phone"

        return jsonify({
            "reply":"Please enter your phone number."
    })

    if user_state.get("step") == "donor_phone":

        donation_data["phone"] = user_message

        user_state["step"] = "donation_amount"

        return jsonify({
            "reply":"How much would you like to donate?"
    })


    if user_state.get("step") == "donation_amount":

        donation_data["amount"] = user_message

        user_state["step"] = "donation_cause"

        return jsonify({
            "reply":"""
    Which cause would you like to support?

    1. Education
    2. Food Distribution
    3. Women Empowerment
    """
    })

    if user_state.get("step") == "donation_cause":

        donation_data["cause"] = user_message

        save_donation(
            donation_data["name"],
            donation_data["email"],
            donation_data["phone"],
            donation_data["amount"],
            donation_data["cause"]
        )

        user_state.clear()

        return jsonify({
            "reply":f"""
    Donation Interest Recorded ✅

    Name: {donation_data['name']}
    Email: {donation_data['email']}
    Phone: {donation_data['phone']}
    Amount: ₹{donation_data['amount']}
    Cause: {donation_data['cause']}

    Thank you for supporting NayePankh Foundation!
    """
    })

    # Start Volunteer Registration

    if  "volunteer" in user_message.lower():

        user_state["step"] = "name"

        return jsonify({
            "reply": "Great! Let's register you as a volunteer. What is your full name?"
        })

    # Name

    if user_state.get("step") == "name":

        volunteer_data["name"] = user_message

        user_state["step"] = "email"

        return jsonify({
            "reply": "Please enter your email address."
        })

    # Email

    if user_state.get("step") == "email":

        volunteer_data["email"] = user_message

        user_state["step"] = "phone"

        return jsonify({
            "reply": "Please enter your phone number."
        })

    # Phone

    if user_state.get("step") == "phone":

        volunteer_data["phone"] = user_message

        user_state["step"] = "skills"

        return jsonify({
            "reply": "What skills do you have?"
        })

    # Skills

    if user_state.get("step") == "skills":

        volunteer_data["skills"] = user_message

        user_state["step"] = "hours"

        return jsonify({
            "reply": "How many hours per week can you volunteer?"
        })

    # Hours

    if user_state.get("step") == "hours":

        volunteer_data["hours"] = user_message
        
        # ------add database  save-----------
        save_volunteer(
            volunteer_data["name"],
            volunteer_data["email"],
            volunteer_data["phone"],
            volunteer_data["skills"],
            volunteer_data["hours"]
        )
        user_state.clear()

        return jsonify({
            "reply": f"""
            Volunteer Registration Completed ✅

Name: {volunteer_data['name']}

Email: {volunteer_data['email']}

Phone: {volunteer_data['phone']}

Skills: {volunteer_data['skills']}

Availability: {volunteer_data['hours']} hours/week

Thank you for joining NayePankh Foundation!
"""
        })

    # return jsonify({
    #     "reply": "You can ask about volunteering, donations, or NGO programs."
    # })

    ai_reply = ask_gemini(user_message)
    return jsonify({
        "reply": ai_reply
})

@app.route("/admin")
def admin():

    print("ADMIN ROUTE HIT")
    volunteers = get_volunteers()

    donations=get_donations()
    
    total_volunteers =volunteer_count()

    total_donations = donation_count()

    return render_template(
        "admin.html",
        volunteers=volunteers,
        donations=donations,
        total_volunteers=total_volunteers,
        total_donations=total_donations
    )

# --------------save info-----------------
def save_volunteer(name, email, phone, skills, hours):

        conn = sqlite3.connect("volunteers.db")

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO volunteers
        (name, email, phone, skills, hours)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, skills, hours))
        conn.commit()
        conn.close()

    # ----------donation----------
def save_donation(name, email, phone, amount, cause):

        conn = sqlite3.connect("volunteers.db")

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO donations
        (name, email, phone, amount, cause)
        VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, amount, cause))

        conn.commit()
        conn.close()

def get_volunteers():

        conn = sqlite3.connect("volunteers.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteers")
        volunteers = cursor.fetchall()
        conn.close()
        return volunteers
    

def get_donations():

        conn = sqlite3.connect("volunteers.db")

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM donations")

        donations = cursor.fetchall()

        conn.close()

        return donations
    
    # volunteer count

def volunteer_count():

        conn = sqlite3.connect("volunteers.db")

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM volunteers")

        count = cursor.fetchone()[0]

        conn.close()

        return count

 # donation count
def donation_count():

    conn = sqlite3.connect("volunteers.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM donations")

    count = cursor.fetchone()[0]

    conn.close()

    return count
    
# create Ai function

def ask_gemini(prompt):

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"

   

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
