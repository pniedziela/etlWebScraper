from flask import Flask
from flask import render_template
from flask import request
from Scraper import *
from flask import send_from_directory
from Transform import *


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def render_home():
    if request.method == 'GET':
        return render_template('main.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    req = request.form
    pages = int(req.get("pages"))
    scraper = WebScraper(pages)
    scraper.run()
    scResults =scraper.results
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
