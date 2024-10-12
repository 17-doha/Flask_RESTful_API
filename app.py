from flask import Flask
from routes.students import students_bp
app = Flask(__name__)

app.register_blueprint(students_bp, url_prefix="/students")

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error":"Resource not found"}), 404

if __name__ == '__main__':
    app.run()