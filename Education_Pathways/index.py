# this is the flask core

from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api,Resource, reqparse
# from flask_pymongo import PyMongo
import os
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

import pandas as pd
df = pd.read_csv("resources/courses.csv", keep_default_na=False, na_values=['_'])
mnrs = pd.read_csv("resources/minorDB.csv")


import config
app = Flask(__name__, static_folder='frontend/build')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# MongoDB URI
# app.config["MONGO_URI"] = "mongodb://root:example@mongo:27017/EducationPathways?readPreference=primary&tls=false"
# mongo = PyMongo(app)

config.init_app(app)
config.init_db(app)
config.init_cors(app)

conn = TinyDB(storage=MemoryStorage)
conn2 = TinyDB(storage=MemoryStorage)

from collections import defaultdict
related = defaultdict(list)
for index, row in df.iterrows():
    course = row['Code']
    prereq = row['Pre-requisites'][1:-1].replace("\'","").replace(" ","")
    if(prereq == ""):
        prereq = []
    else:
        prereq = prereq.split(",")
    for pr in prereq:
        related[pr].append(course)

def formatListToStr(str):
    return str[1:-1].replace("\'","").split(",")

# route functions
def search_course_by_code(s):
    # return all the courses whose course code contains the str s
    course_ids = df[df['Code'].str.contains(s.upper())].index.tolist()
    if len(course_ids) == 0:
        return []
    if len(course_ids) > 10:
        course_ids = course_ids[:10]
    res = []
    for i, course_id in enumerate(course_ids):
        d = df.iloc[course_id].to_dict()
        related_course = related[d['Code']]
        related_course.sort()
        print(d['Professors'])
        res_d = {
            '_id': i,
            'code': d['Code'],
            'name': d['Name'],
            'division': d['Division'],
            'department': d['Department'],
            'description': d['Course Description'],
            'syllabus': "Course syllabus here.",
            'prereq': formatListToStr(d['Pre-requisites']),
            'coreq': formatListToStr(d['Corequisite']),
            'related': ", ".join(related_course),
            'exclusion': formatListToStr(d['Exclusion']),
            'professors': d['Professors'],
            'hours': d['Hours'],
            'term': d['Term'],
        }
        res.append(res_d)
    return res
            
            
            
class SearchCourse(Resource):
    def get(self):
        input = request.args.get('input')
        courses = search_course_by_code(input)
        print(courses)
        # courses =[{'_id': 1, 'code': 'ECE444', 'name': 'SE'}, {'_id': 2,'code': 'ECE333', 'name': 'ur mom'}]
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {input} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify(courses)
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': str(e)})
            resp.status_code = 400
            return resp

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('input', required=True)
        data = parser.parse_args()
        input = data['input']
        courses = search_course_by_code(input)
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {input} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify(courses)
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 400
            return resp

class ShowCourse(Resource):
    def get(self):
        code = request.args.get('code')
        courses = search_course_by_code(code)
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 400
            return resp
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        data = parser.parse_args()
        code = data['code']
        courses = search_course_by_code(code)
        if len(courses) == 0:
            resp = jsonify({'message': f"Course {code} doesn't exist"})
            resp.status_code = 404
            return resp
        try:
            resp = jsonify({'course': courses[0]})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({'error': 'something went wrong'})
            resp.status_code = 400
            return resp

class Reviews(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', required=True, location='args')
        data = parser.parse_args()
        reviews = conn.search(Query().course == data["course"])
        print(reviews)
        return jsonify(reviews)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', required=True, location='args')
        parser.add_argument('description', required=True, location='json')
        parser.add_argument('rating', required=True, location='json')
        data = parser.parse_args()
        conn.insert({"course": data["course"], "description": data["description"], "rating": data["rating"]})
        print(conn.all())
        return {}

class Recommendations(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course1', required=True, location='args')
        data = parser.parse_args()
        recomm = conn2.search(Query().course1 == data["course1"])
        print(recomm)
        return jsonify(recomm)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course1', required=True, location='json')
        parser.add_argument('course2', required=True, location='json')
        parser.add_argument('description', required=True, location='json')
        data = parser.parse_args()
        conn2.insert({"course1": data["course1"], "course2": data["course2"], "description": data["description"]})
        conn2.insert({"course1": data["course2"], "course2": data["course1"], "description": data["description"]})
        print(conn2.all())
        return {}

class ShowCourseValid(Resource):
    def get(self):
        return
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseOrig', required=True, location='json')
        parser.add_argument('courseCheck', required=True, location='json')
        data = parser.parse_args()
        check = data['courseCheck'].upper()
        check = check.strip()
        if('H1' not in check):
            check = check + "H1"
        print(check)
        if(len(df.loc[df['Code'] == check]) > 0):
            resp = jsonify({'course': check})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'course': ""})
            resp.status_code = 404
            return resp

def search_for_minor_prescence(s):
    course_id = mnrs[mnrs['course'].str.contains(s.upper())].index.tolist()
    if len(course_id) == 0:
        return []
    if len(course_id) > 1:
        print("Something went wrong!")
        return []
    d = mnrs.iloc[course_id].to_dict()
    res= {
        'Advanced Manufacturing': d['AdvMan'],
        'Artificial Intelligence Engineering': d['AIEng'],
        'Biomedical Engineering': d['BioMedEng'],
        'Engineering Business': d['EngBusiness'],
        'Environmental Engineering': d['EnviroEng'],
        'Nanoengineering': d['NanoEng'],
        'Robotics and Mechatronics': d['RbtsNMech'],
        'Sustainable Energy': d['SusEnergy'],
    }
    return res

def generateEngMinorData(s):
    courseInfo = search_for_minor_prescence(s)
    if len(courseInfo) == 0:
            return {'minorInfo': "This course is not part of any engineering minor."}
    finalString = ""
    for key in courseInfo:
        if('Y' in courseInfo[key].values()): 
            finalString += f" {key},"
    return {'minorInfo': f"This course is part of the following minors:{finalString[:-1]}."}

class Minors(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course', required=True, location='args')
        data = parser.parse_args()
        minorDescription = generateEngMinorData(data.course);
        return jsonify(minorDescription)
            
    #this API has no post method, used for GET requests only        
    def post(self):
        return {}

# API Endpoints
rest_api = Api(app)
# rest_api.add_resource(controller.SearchCourse, '/searchc')
rest_api.add_resource(SearchCourse, '/searchc')
# rest_api.add_resource(controller.ShowCourse, '/course/details')
rest_api.add_resource(ShowCourse, '/course/details')
rest_api.add_resource(Reviews, '/reviews')
rest_api.add_resource(Recommendations, '/recommendations')
rest_api.add_resource(ShowCourseValid, '/test')
rest_api.add_resource(Minors, '/minors')

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, extra_files=['app.py', 'controller.py', 'model.py'])
    app.run(threaded=True, port=5000)
    # with open("test.json") as f:
    #     data = json.load(f)
    # for i in range(75):
    #     i = str(i)
    #     Course(name=data["name"][i], code=data["code"][i], description=data["description"][i], prereq=data["prereq"][i], coreq=data["coreq"][i], exclusion=data["exclusion"][i]).save()

    
    
