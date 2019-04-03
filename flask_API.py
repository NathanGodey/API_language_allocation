from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bson.json_util
import json
import pymongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'language_allocation_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/language_allocation_database'

mongo = PyMongo(app)


def get_max_course_id():
    return int(mongo.db.courses.find_one(sort=[("id", -1)])["id"])

@app.route('/courses/<course_id>', methods=['GET'])
def get_course_by_id(course_id):
    courses = mongo.db.courses
    course = courses.find_one({"id": int(course_id)})
    if course:
        output={}
        output["id"] = course["id"]
        output["name"] = course["name"]
        output["language"] = course["language"]
        output["creneaux"] = course["creneaux"]
        output["min_students"] = course["min_students"]
        output["max_students"] = course["max_students"]
        html_code = 200
    else:
        output = "No matching course for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/by-language/<language>', methods=['GET'])
def get_course_by_language(language):
    courses = mongo.db.courses
    courses_of_language = courses.find({"language": language})
    if courses_of_language:
        Output = []
        for course in courses_of_language:
            output={}
            output["id"] = course["id"]
            output["name"] = course["name"]
            output["language"] = course["language"]
            output["creneaux"] = course["creneaux"]
            output["min_students"] = course["min_students"]
            output["max_students"] = course["max_students"]
            Output.append(output)
        html_code = 200
    else:
        Output = "No matching course for language " + str(language)
        html_code = 400
    return jsonify({'result': Output}), html_code

@app.route('/courses/not-english/', methods=['GET'])
def get_course_not_english():
    courses = mongo.db.courses
    Output = []
    for course in courses_of_language:
        if course["language"] != "Anglais":
            output={}
            output["id"] = course["id"]
            output["name"] = course["name"]
            output["language"] = course["language"]
            output["creneaux"] = course["creneaux"]
            output["min_students"] = course["min_students"]
            output["max_students"] = course["max_students"]
            Output.append(output)
        html_code = 200
    return jsonify({'result': Output}), html_code


@app.route('/courses/<course_id>', methods=['POST'])
def update_course(course_id):
    courses = mongo.db.courses
    new_name = request.get_json(force=True)['name']
    new_language = request.get_json(force=True)['language']
    new_creneaux = request.get_json(force=True)['creneaux']
    new_min_students = request.get_json(force=True)['min_students']
    new_max_students = request.get_json(force=True)['max_students']
    course_update = courses.update({"id":int(course_id)}, {"id":int(course_id),
                                                           "name":new_name,
                                                           "language":new_language,
                                                           "creneaux":new_creneaux,
                                                           "min_students":new_min_students,
                                                           "max_students":new_max_students})
    if course_update:
        output = "Course with id "+course_id+" updated successfully"
        html_code = 200
    else:
        output = "No matching course for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/', methods=['PUT'])
def add_course():
    courses = mongo.db.courses
    id = get_max_course_id()+1
    new_name = request.get_json(force=True)['name']
    new_language = request.get_json(force=True)['language']
    new_creneaux = request.get_json(force=True)['creneaux']
    new_min_students = request.get_json(force=True)['min_students']
    new_max_students = request.get_json(force=True)['max_students']
    course_inserted = courses.insert({"id":int(id),
                                                           "name":new_name,
                                                           "language":new_language,
                                                           "creneaux":new_creneaux,
                                                           "min_students":new_min_students,
                                                           "max_students":new_max_students})
    if course_inserted:
        output = {"id":id}
        html_code = 200
    else:
        output = "Could not add course"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/courses/<course_id>', methods=['DELETE'])
def remove_course(course_id):
    courses = mongo.db.courses
    course_removed = courses.remove({"id":int(course_id)})
    if course_removed:
        output = "Course successfully removed"
        html_code = 200
    else:
        output = "Could not remove course"
        html_code = 400
    return jsonify({'result': output}), html_code





@app.route('/creneaux/<creneaux_id>', methods=['GET'])
def get_creneau_by_id(creneau_id):
    creneaux = mongo.db.creneaux
    creneau = creneaux.find_one({"id": int(creneau_id)})
    if creneau:
        output={}
        output["id"] = creneau["id"]
        output["day"] = creneau["day"]
        output["begin"] = creneau["begin"]
        output["end"] = creneau["end"]
        output["type"] = creneau["type"]
        html_code = 200
    else:
        output = "No matching creneau for id " + str(course_id)
        html_code = 400
    return jsonify({'result': output}), html_code

@app.route('/creneaux/by-promotion/<promo>', methods=['GET'])
def get_creneau_by_promo(promo):
    creneaux = mongo.db.creneaux.find()
    Output = []
    for creneau in creneaux:
        if promo in creneau["type"]:
            output={}
            output["id"] = creneau["id"]
            output["day"] = creneau["day"]
            output["begin"] = creneau["begin"]
            output["end"] = creneau["end"]
            output["type"] = creneau["type"]
            Output.append(output)
        html_code = 200
    return jsonify({'result': Output}), html_code


@app.route('/creneaux/<creneau_id>', methods=['POST'])
def update_creneau(creneau_id):
    creneaux = mongo.db.creneaux
    new_day = request.get_json(force=True)['day']
    new_begin = request.get_json(force=True)['begin']
    new_end = request.get_json(force=True)['end']
    new_type = request.get_json(force=True)['type']
    creneau_updated = courses.update({"id":int(creneau_id)}, {"id":int(creneau_id),
                                                           "day":new_day,
                                                           "begin":new_begin,
                                                           "end":new_end,
                                                           "type":new_type})
    if creneau_updated:
        output = "Creneau with id "+creneau_id+" updated successfully"
        html_code = 200
    else:
        output = "No matching creneau for id " + str(creneau_id)
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/creneaux/', methods=['PUT'])
def add_creneau():
    creneaux = mongo.db.creneaux
    id = get_max_course_id()+1
    new_day = request.get_json(force=True)['day']
    new_begin = request.get_json(force=True)['begin']
    new_end = request.get_json(force=True)['end']
    new_type = request.get_json(force=True)['type']
    creneau_inserted = courses.insert({"id":int(creneau_id),
                                                           "day":new_day,
                                                           "begin":new_begin,
                                                           "end":new_end,
                                                           "type":new_type})
    if course_inserted:
        output = {"id":id}
        html_code = 200
    else:
        output = "Could not add course"
        html_code = 400
    return jsonify({'result': output}), html_code


@app.route('/creneaux/<creneau_id>', methods=['DELETE'])
def remove_creneau(creneau_id):
    creneaux = mongo.db.creneaux
    creneau_removed = creneaux.remove({"id":int(creneau_id)})
    if creneau_removed:
        output = "Creneau successfully removed"
        html_code = 200
    else:
        output = "Could not remove creneau"
        html_code = 400
    return jsonify({'result': output}), html_code

if __name__ == '__main__':
    app.run(debug=True)
