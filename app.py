from flask import Flask, render_template, json
import os

app = Flask(__name__)

# helper function to load data
def load_menu():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_directory, 'menu.json')
    with open(json_path, 'r') as file:
        menu_data = json.load(file)

    # access items key
    items = menu_data['items']

    # categorise items
    food_items = [item for item in items if item['category'] == 'Food']
    drink_items = [item for item in items if item['category'] == 'Drinks']
    
    return food_items, drink_items

# route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# route for menu page
@app.route("/menu")
def menu():
    food_items, drink_items = load_menu()
    return render_template("menu.html", food_items=food_items, drink_items=drink_items)

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
