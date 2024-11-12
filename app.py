from flask import Flask, render_template
import json
import os

app = Flask(__name__)

# helper function to load data
def load_menu():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_directory, 'menu.json')
    with open(json_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data['items']

# route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# route for menu page
@app.route("/menu")
def menu():
    items = load_menu()
    return render_template("menu.html", items=items)

# route for about us page
@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

# route for reservations
@app.route("/reservations")
def reservations():
    return render_template("reservations.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
