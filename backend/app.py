from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import tempfile

# Allow importing files from src
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_DIR = os.path.join(PROJECT_ROOT, "src")

sys.path.insert(0, SRC_DIR)

from predict import predict_image


app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Handwriting Digitizer API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Check uploaded file
        if "image" not in request.files:

            return jsonify({
                "success": False,
                "error": "No image uploaded"
            }), 400

        image = request.files["image"]

        if image.filename == "":

            return jsonify({
                "success": False,
                "error": "No image selected"
            }), 400

        # Temporary image
        suffix = os.path.splitext(
            image.filename
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:

            image.save(temp.name)

            temp_path = temp.name

        # Run handwriting recognition
        text = predict_image(
            temp_path
        )

        # Delete temporary file
        os.remove(temp_path)

        return jsonify({
            "success": True,
            "text": text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )