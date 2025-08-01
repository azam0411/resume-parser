from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from resume_parser import parse_resume
from translator import translate_content
from currency import get_price_by_country

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    structured_data = parse_resume(filepath)
    return jsonify(structured_data)


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    content = data.get('content')
    target_lang = data.get('lang')

    if not content or not target_lang:
        return jsonify({'error': 'Content and lang are required'}), 400

    translated = translate_content(content, target_lang)
    return jsonify({'translated': translated})


@app.route('/get-price', methods=['GET'])
def get_price():
    country = request.args.get('country')
    if not country:
        return jsonify({'error': 'Country is required'}), 400

    pricing_info = get_price_by_country(country)
    return jsonify(pricing_info)


if __name__ == '__main__':
    app.run(debug=True)
