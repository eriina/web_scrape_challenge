from flask_pymongo import PyMongo
from flask import Flask, render_template
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
# import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
# conn = 'mongodb://localhost:27017'
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_db'
# Pass connection to the pymongo instance.
# mongo = pymongo.MongoClient(conn)
mongo = PyMongo(app)
# Connect to a database. Will create one if not already available.
# db = mongo.mars_db

# Drops collection if available to remove duplicates
# db.mars.drop()

# Set route
@app.route('/scrape')
def scrape():
    # Store the entire team collection in a list
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
       {},
        mars_data,
        upsert=True
    )
    return "Scrapping Successful"

@app.route('/')
def index():
    # Return the template with the teams list passed in
    mars=mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
