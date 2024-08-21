from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import datetime
import smtplib
import os
from dotenv import load_dotenv

# App creation
app = Flask(__name__)
app.config["Secret Key"] = os.getenv("SECRET_KEY")
Bootstrap(app)
# Data showing in the footer
current_year = datetime.datetime.today().year
# Data for the email for the contact page
load_dotenv() 
app_pass = os.getenv("APP_PASS")
email_studio = os.getenv("EMAIL_STUDIO")

def send_emails(body):
     subject = "Morse Code Contact Info!"
     message = "subject:{}\n\n{}".format(subject,body)
     #GET THE EMAIL USERS IN A LIST
     with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email_studio, password=app_pass)
        connection.sendmail(from_addr=email_studio,
                                   to_addrs=email_studio,
                                    msg=message)



# Code for the morse code translator
# Variable to join the str chain
joined_morse_code = ''
# MORSE CODE ALPHABET.
normal_to_morse = {"a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....",
                   "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.",
                   "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
                   "y": "-.--", "z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....",
                   "7": "--...", "8": "---..", "9": "----.", "0": "-----", " ": " "}
# MORSE CODE TO ALPHABET
morse_to_normal = {normal_to_morse[value]: value for (value) in normal_to_morse}
control_list = [key for key in normal_to_morse]
control_list2 = [key for key in morse_to_normal]


def traduce(x):
        # CHANGE TO MORSE CODE
        try:
            str = " "
            user_text = list(x)  # USER INPUT TO LIST
            morse_code = [normal_to_morse[letter] for letter in
                            user_text]  # TAKE THE VALUES FROM THE DICTIONARY WITH THE SAME KEY
            joined_morse_code = str.join(morse_code)  # MAKE IT A STRING TO PRINT TO THE USER
            return joined_morse_code
        # CHANGE TO NORMAL ALPHABET
        except KeyError:
            str = ""
            user_text2 = x.split()  # USER INPUT TO LIST. SPLIT WITHIN THE BLANK SPACES
            try:
                normal_alphabet = [morse_to_normal[code] for code in
                                    user_text2]  # TAKE THE VALUES FROM THE DICTIONARY WITH THE SAME KEY
                joined_morse_code = str.join(normal_alphabet)
                return joined_morse_code  # PRINT IN THE INSERT TOOL
            # pass if the char input is not in the list
            except KeyError:
                pass

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
           text = str(request.form.get('textarea')).lower()
           text2 = traduce(text)
    try:       
        return render_template("index.html", year=current_year, new_text=text2)
    except:
        return render_template("index.html", year=current_year, new_text=None)
    
@app.route('/contact',  methods=["GET", "POST"])
def contact():
    if request.method == "POST":
         message = request.form.get('message')
         name = request.form.get('name')
         email = request.form.get('email')
         phone_number = request.form.get('phone')
         #print(message, name, email, phone_number)
         send_emails(f"Hi!\n"
                     f"User name: {name}, \n"
                     f"Us phone number: {phone_number}\n"
                     f"User email: {email}\n"
                     f"User message: {message}")
         return render_template("send.html")
    return render_template("contact.html", year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
