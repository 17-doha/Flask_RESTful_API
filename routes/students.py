from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token

students_bp = Blueprint("students", __name__)

students = []

@students_bp.before_request
def before_request():
    authenticate_token()

@students_bp.route("/", methods = ["GET"])
def get_students():
    return jsonify(students)

@students_bp.route("/<int:id>", methods = ["GET"])
def get_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)



@students_bp.route("/", methods = ["POST"])
def create_student():
    name = request.json.get("name")
    major = request.json.get("major")
    if not name or not major:
        return jsonify({"error": "Missing required fields: 'name' and 'major' are required"}), 400
    
    student = {
        "id" : len(students) + 1,
        "name" : name,
        "major": major,
        "status": request.json.get("status", "Undergraduate"),
    }
    students.append(student)
    return jsonify(student), 201

@students_bp.route("/<int:id>", methods = ["PUT"])
def update_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if student is None:
        return jsonify({"error":"Student not found"}), 404
    student["major"] = request.json.get("major", student["major"])
    student["status"] = request.json.get("status", student["status"])
    return jsonify(student)

@students_bp.route("/<int:id>", methods = ["DELETE"])
def delete_student(id):
    global students
    student = next((s for s in students if s["id"] == id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    
    students = [s for s in students if s["id"] != id] 
    return '', 204