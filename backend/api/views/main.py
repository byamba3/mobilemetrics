from api import app
from flask import Blueprint
#from api.utils import create_response, serialize_list
from api.project import analyze
from flask import jsonify, request, Response
from api.utils import create_response, serialize_list

mod = Blueprint('main', __name__)


# function that is called when you visit /
@app.route('/')
def index(): 
    return '<h1>Hello World!</h1>'

@app.route('/analyze', methods=['POST'])
def analyze_data():
    query = request.get_json()
    print(query)
    if query == None or query == {} or query['phoneType'] == '':
        return create_response(data={'performance': None,
        'battery': None,
        'display': None,
        'camera': None,
        'overall': None,
        'articles': None}, status =200)
    
    analyzedOutput = analyze(query)
    articles = [article.serialize() for article in analyzedOutput[5]]
    return create_response(data={'performance': analyzedOutput[0], 
    'battery': analyzedOutput[1], 
    'display': analyzedOutput[2], 
    'camera': analyzedOutput[3], 
    'overall': analyzedOutput[4],
    'articles': articles}, status =200)