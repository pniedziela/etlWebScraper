from flask import Flask
from flask import render_template
from flask import request
from Scraper import *
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
import itertools
import re


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
    area = db.Column(db.Numeric(precision=2))

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
    # for row in db.session.query(ScrapTable.location).all():
    #     print(row)
    locations = db.session.query(ScrapTable.location).all()
    rooms = db.session.query(ScrapTable.rooms).all()
    prices = db.session.query(ScrapTable.price).all()
    area = db.session.query(ScrapTable.area).all()
    result_loc = []
    result_room = []
    result_pric = []
    result_area = []

    # Calculations for locations
    for values in locations:
        for value in values:
            cutted_value = re.search(': (.*),', value).group(1)
            result_loc.append(cutted_value)
    print(result_loc)

    # Calculations for rooms
    for values in rooms:
        for value in values:
            res = value[0]
            result_room.append(int(res))
    print(result_room)

    # Calculation for price

    for values in prices:
        for value in values:
            splited = value.split('z')[0]
            result_pric.append(int(splited))
    print(result_pric)

    # Calculation for area
    for values in area:
        for value in values:
            splited_ar = value.split(' ')[0]
            splited_re = splited_ar.replace(',', '.')
            result_area.append(float(splited_re))
    print(result_area)

    #Database commit part

    for (x, y, z, b) in itertools.zip_longest(result_loc, result_room, result_pric, result_area):
        if db.session.query(TransformTable).filter_by(location=x, rooms=y, price=z, area=b) == None:
            print(db.session.query(TransformTable).filter_by(location=x, rooms=y, price=z, area=b))
            continue
        else:
            data = TransformTable(x, y, z, b)
            db.session.add(data)
            db.session.commit()

    return render_template('transform.html')



@app.route('/load', methods=['GET', 'POST'])
def load():

    locations_tra = db.session.query(TransformTable.location).all()
    rooms_tra = db.session.query(TransformTable.rooms).all()
    prices_tra = db.session.query(TransformTable.price).all()
    area_tra = db.session.query(TransformTable.area).all()

    final_results = []
    for index in range(0, len(locations_tra)):
        final_results.append({
            'location': locations_tra[index],
            'rooms': rooms_tra[index],
            'price': prices_tra[index],
            'area': area_tra[index]
        })

    return render_template('load.html', results=final_results)



if __name__ == '__main__':
    app.run(debug=True, threaded=True)