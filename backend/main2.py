import pymongo
with open('pizza.txt', 'r') as file:
    password = file.read()
client = pymongo.MongoClient(f"mongodb+srv://jsamprith:{password}@cluster0.tmzsn7p.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]
collection = db["mycollection"]
my_document = {"name": "John", "age": 28}
collection.insert_one(my_document)
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


# API endpoints
@app.route('/submit_essay', methods=['POST'])
def submit_essay():
    # Get essay data from request
    essay_data = request.json

    # Insert essay into Essays collection
    essays_collection = db['essays']
    essay_id = essays_collection.insert_one(essay_data).inserted_id

    # Calculate similarity scores
    similarity_scores = []
    essays = list(essays_collection.find())
    for other_essay in essays:
        if other_essay['_id'] != essay_id:
            similarity_score = calculate_similarity(essay_data['content'], other_essay['content'])
            similarity_scores.append(similarity_score)

    # Insert similarity scores into Similarity Matrix collection
    similarity_matrix_collection = db['similarity_matrix']
    similarity_matrix_collection.insert_one({
        'essay_id': str(essay_id),
        'similarity_scores': similarity_scores
    })

    return jsonify({'message': 'Essay submitted successfully!'})

@app.route('/get_marks', methods=['GET'])
def get_marks():
    # Get student ID and essay ID from request
    student_id = request.args.get('student_id')
    essay_id = request.args.get('essay_id')

    # Get marks from Marks collection
    marks_collection = db['marks']
    marks = marks_collection.find_one({'student_id': student_id, 'essay_id': essay_id})

    return jsonify({'marks': marks['marks']})

@app.route('/get_feedback', methods=['GET'])
def get_feedback():
    # Get student ID and essay ID from request
    student_id = request.args.get('student_id')
    essay_id = request.args.get('essay_id')

    # Get feedback from Feedback collection
    feedback_collection = db['feedback']
    feedback = feedback_collection.find_one({'student_id': student_id, 'essay_id': essay_id})

    return jsonify({'feedback': feedback['feedback']})

import random
def calculate_similarity(essay1, essay2):
    return random.random()

def preprocess(essay):
    # Preprocess essay text here
    return essay



@app.route('/get_essays', methods=['GET'])
def get_essays():
    # Get all essays from Essays collection
    essays_collection = db['essays']
    essays = list(essays_collection.find())

    return jsonify({'essays': essays})

@app.route('/grade_essay', methods=['POST'])
def grade_essay():
    # Get grading data from request
    grading_data = request.json

    # Insert grading data into Marks and Feedback collections
    marks_collection = db['marks']
    marks_collection.insert_one({
        'student_id': grading_data['student_id'],
        'essay_id': grading_data['essay_id'],
        'marks': grading_data['marks']
    })

    feedback_collection = db['feedback']
    feedback_collection.insert_one({
        'student_id': grading_data['student_id'],
        'essay_id': grading_data['essay_id'],
        'feedback': grading_data['feedback']
    })

    return jsonify({'message': 'Essay graded successfully!'})

@app.route('/add_essay', methods=['POST'])
def add_essay():
    # Get essay data from request
    essay_data = request.json

    # Insert essay into Essays collection
    essays_collection = db['essays']
    essay_id = essays_collection.insert_one(essay_data).inserted_id

    return jsonify({'message': 'Essay added successfully!', 'essay_id': str(essay_id)})

@app.route('/get_student', methods=['GET'])
def get_student():
    # Get student ID from request
    student_id = request.args.get('student_id')

    # Get student from Students collection
    students_collection = db['students']
    student = students_collection.find_one({'_id': student_id})

    return jsonify({'student': student})

@app.route('/get_teacher', methods=['GET'])
def get_teacher():
    # Get teacher ID from request
    teacher_id = request.args.get('teacher_id')

    # Get teacher from Teachers collection
    teachers_collection = db['teachers']
    teacher = teachers_collection.find_one({'_id': teacher_id})

    return jsonify({'teacher': teacher})

@app.route('/get_student_essays', methods=['GET'])
def get_student_essays():
    # Get student name from request
    student_name = request.args.get('student_name')

    # Get student ID from Students collection
    students_collection = db['students']
    student = students_collection.find_one({'name': student_name})
    student_id = student['_id']

    # Get essays written by student from Essays collection
    essays_collection = db['essays']
    essays = list(essays_collection.find({'student_id': student_id}))

    return jsonify({'essays': essays})

@app.route('/get_essay', methods=['GET'])
def get_essay():
    # Get essay ID from request
    essay_id = request.args.get('essay_id')

    # Get essay from Essays collection
    essays_collection = db['essays']
    essay = essays_collection.find_one({'_id': ObjectId(essay_id)})

    if essay:
        return jsonify({'essay': essay})
    else:
        return jsonify({'message': 'Essay not found.'}), 404
    
@app.route('/get_assignments', methods=['GET'])
def get_assignments():
    # Get teacher name from request
    teacher_name = request.args.get('teacher_name')

    # Get essays assigned by the teacher from Essays collection
    essays_collection = db['essays']
    assigned_essays = list(essays_collection.find({'teacher': teacher_name}))

    if assigned_essays:
        return jsonify({'assigned_essays': assigned_essays})
    else:
        return jsonify({'message': 'No essays assigned by the specified teacher.'}), 404




if __name__ == '_main_':
    app.run()