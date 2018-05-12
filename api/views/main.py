from api import app
from flask import Blueprint
from api.models import Person
from project import create_response, serialize_list
from api.utils import create_response, serialize_list
from api.project import analyze
from flask import jsonify

mod = Blueprint('main', __name__)


# function that is called when you visit /
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


# function that is called when you visit /persons
@app.route('/persons')
def name():
    try:
        persons = Person.query.all()
        persons_list = serialize_list(persons)   
        return create_response(data={'persons': persons_list})
    except Exception as ex:
        return create_response(data={}, status=400, message=str(ex))

@app.route('/analyze', methods=['GET'])
def analyze_data(query):
    print(query)
    analyzedOutput = analyze(query)
    return jsonify(averagePerformance = analyzedOutput[0], 
    averageBattery = analyzedOutput[1], 
    averageDisplay = analyzedOutput[2], 
    averageCamera = analyzedOutput[3], 
    averageOverall = analyzedOutput[4],
        articles = [article.serialize() for article in analyzedOutput[5]])