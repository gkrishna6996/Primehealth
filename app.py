from flask_mail import Mail, Message
from flask import Flask, render_template, request, jsonify, render_template_string
import sqlite3


app = Flask(__name__)
# --- Ye configuration Line 7 se start karein ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gkrishna6996@gmail.com' # Apna Gmail yahan likhein
app.config['MAIL_PASSWORD'] = 'wgeg oakw ivcp wnpk' # 16 digit ka App Password
mail = Mail(app)
# Create database automatically
conn = sqlite3.connect('appointments.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT
)
''')

conn.commit()
conn.close()


# SINGLE FILE WEBSITE (HTML + CSS + JS inside Python)
HTML_PAGE = """

<!DOCTYPE html>
<html>
<head>
    <title>Prime Smart Health Care</title>
    <style>
        body { font-family: Arial; margin:0; background:#f4f8fb; }
        header{ background:#0a6ebd; color:white; padding:20px; text-align:center; }
        nav{ background:#0c8f6a; padding:15px; text-align:center; }
        nav a{ color:white; margin:15px; text-decoration:none; font-weight:bold; }
        .hero{ text-align:center; padding:50px; }
        .hero button{ padding:15px; background:#0a6ebd; color:white; border:none; font-size:18px; cursor:pointer; }
        section{ padding:40px; background:white; margin:20px; border-radius:10px; }
        form input, form select{ display:block; margin:10px auto; padding:12px; width:300px; }
        button{ background:green; color:white; padding:12px; border:none; cursor:pointer; }
        footer{ background:#0a6ebd; color:white; text-align:center; padding:20px; }
    </style>
</head>
<body>
    <header>
        <h1>Prime Smart Health Care</h1>
        <p>Reliable Care. Trained Hands.</p>
        <p>Email: primesmarthealthcare@aol.com</p>
    </header>

    <nav>
        <a href="#">Home</a>
        <a href="#services">Services</a>
        <a href="#appointment">Book Appointment</a>
        <a href="#contact">Contact</a>
    </nav>

    <div class="hero">
        <h2>Hospital-Level Care at Your Home</h2>
        <p>ICU Care | Elder Care | Nursing Staff</p>
        <button onclick="scrollToAppointment()">Book Appointment</button>
    </div>

    <section id="services">
        <h2>Our Services</h2>
        <ul>
            <li>24x7 Doctor Support</li>
            <li>ICU at Home</li>
            <li>Elder Care</li>
            <li>Nursing Staff</li>
            <li>Physiotherapy</li>
            <li>Medical Equipment</li>
        </ul>
    </section>

    <section id="appointment">
        <h2>Book Appointment</h2>
        <form onsubmit="bookAppointment(event)">
            <input type="text" id="name" placeholder="Full Name" required>
            <input type="number" id="age" placeholder="Age" required>
            <input type="text" id="phone" placeholder="Phone Number" required>
            <select id="service">
                <option>Elder Care</option>
                <option>ICU at Home</option>
                <option>Nursing Staff</option>
                <option>Physiotherapy</option>
            </select>
            <input type="date" id="date" required>
            <input type="time" id="time" required>
            <button type="submit" class="btn">Submit</button>
        </form>
        <p id="message" style="text-align:center; font-weight:bold;"></p>
    </section>

    <section id="contact">
        <h2>Contact</h2>
        <p>Gurmit Dhiman: 9034385357</p>
        <p>Anu Sharma: 9217356338</p>
        <p>Mamta Dhawan: 9217356339</p>
        <p>Address: 1001 Tower 2, Pareena Micasa Sec. 68, Gurugram</p>
    </section>

    <footer>
        <p>© 2026 Prime Smart Health Care</p>
    </footer>

    <script>
        function scrollToAppointment() {
            document.getElementById('appointment').scrollIntoView({ behavior: 'smooth' });
        }

        function bookAppointment(e) {
            e.preventDefault();
            const msgTag = document.getElementById("message");
            msgTag.innerHTML = "Processing...";

            const data = {
                name: document.getElementById("name").value,
                age: document.getElementById("age").value,
                phone: document.getElementById("phone").value,
                service: document.getElementById("service").value,
                date: document.getElementById("date").value,
                time: document.getElementById("time").value
            };

            fetch("/book", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                msgTag.innerHTML = result.message;
                msgTag.style.color = "green";
                e.target.reset(); // Clears form after success
            })
            .catch(error => {
                console.error('Error:', error);
                msgTag.innerHTML = "❌ Error. Check Terminal.";
                msgTag.style.color = "red";
            });
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/book", methods=["POST"])
def book():
    try:
        data = request.json
        
        # Database Insertion
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (name, age, phone, service, date, time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data["name"], data["age"], data["phone"], data["service"], data["date"], data["time"]))
        conn.commit()
        conn.close()

        # Email Preparation
        msg = Message("New Appointment - Prime Smart Health Care",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=["gkrishna6996@gmail.com"])
        
        msg.body = f"New Booking!\n\nName: {data['name']}\nPhone: {data['phone']}\nService: {data['service']}\nDate: {data['date']}\nTime: {data['time']}"
        
        mail.send(msg)
        return jsonify({"message": "✅ Appointment Booked & Email Sent!"})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"message": f"❌ Error: {str(e)}"}), 500
    
@app.route("/admin")
def admin_panel():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    # Database se saari bookings nikalna
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    
    # Ye data admin.html page ko bhej rahe hain
    return render_template("admin.html", bookings=rows)

if __name__ == "__main__":
    import os
    # Render default mein port provide karta hai, agar nahi toh 5000 use hoga
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' hona sabse zaroori hai Render ke liye
    app.run(host='0.0.0.0', port=port)
