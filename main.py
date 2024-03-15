import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
# database migrations
from model.users import initUsers
from model.players import initPlayers

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io']:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# Read the CSV file into a DataFrame
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('funny.csv')

# Input your stats
your_gpa = float(input("Enter your GPA: "))
your_sat_score = int(input("Enter your SAT score: "))
your_extracurricular_activities = int(input("Enter your number of extracurricular activities: "))

# Calculate average admission rate for each category
accepted_rate = df[df['Admission_Status'] == 'Accepted'].shape[0] / df.shape[0]
rejected_rate = df[df['Admission_Status'] == 'Rejected'].shape[0] / df.shape[0]
waitlisted_rate = df[df['Admission_Status'] == 'Waitlisted'].shape[0] / df.shape[0]

# Determine admission status based on averages
if (your_gpa >= df['GPA'].mean()) and (your_sat_score >= df['SAT_Score'].mean()) and (your_extracurricular_activities >= df['Extracurricular_Activities'].mean()):
    print("Congratulations! You are likely to get in.")
elif (your_gpa < df['GPA'].mean() * 0.8) or (your_sat_score < df['SAT_Score'].mean() * 0.8) or (your_extracurricular_activities < df['Extracurricular_Activities'].mean() * 0.8):
    print("Unfortunately, you are likely to be rejected.")
else:
    print("You are likely to be waitlisted.")
