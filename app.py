from flask import Flask
from flask import render_template
from flask import request
from Scraper import *
from flask import send_from_directory
from Transform import *
from flask_sqlalchemy import SQLAlchemy
import itertools


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thatisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Banana6543210@localhost/ETLdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ScrapTable(db.Model):
    __tablename__ = 'ScrapTable'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))
    rooms = db.Column(db.String(200))
    price = db.Column(db.String(200))
    area = db.Column(db.String(200))

    def __init__(self, location, rooms, price, area):
        self.location = location
        self.rooms = rooms
        self.price = price
        self.area = area

class TransformTable(db.Model):
    __tablename__ = 'TransformTable'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    rooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    area = db.Column(db.Float(precision=2))

    def __init__(self, location, rooms, price, area):
        self.location = location
        self.rooms = rooms
        self.price = price
        self.area = area

@app.route('/', methods=['GET', 'POST'])
def render_home():
    if request.method == 'GET':
        db.session.query(ScrapTable).delete()
        db.session.commit()
        return render_template('main.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    req = request.form
    pages = int(req.get("pages"))
    scraper = WebScraper(pages)
    scraper.run()
    scResults =scraper.results
    loc = [sub['location'] for sub in scResults]
    pri = [sub['price'] for sub in scResults]
    are = [sub['area'] for sub in scResults]
    roo = [sub['rooms'] for sub in scResults]
    for (a, b, c, d) in itertools.zip_longest(loc, roo, pri, are):
        data = ScrapTable(a, b, c, d)
        db.session.add(data)
        db.session.commit()
    return render_template('home.html', extracted=scResults)

@app.route('/download')
def download():
    return send_from_directory('', 'all_offers.csv', as_attachment=True)

@app.route('/transform', methods=['GET', 'POST'])
def transform():
    transformFunc = Transform(scResults)
    transformFunc.run()
    trResult = transformFunc.result
    return  render_template('transform.html', transformed=trResult)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
