# External Imports
from flask import Flask, render_template

# Local Imports
from database import db, Employees, Users, Credentials, Drinks, Ingredients

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///6shot_db.db'
db.init_app(app)
db.app = app

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
