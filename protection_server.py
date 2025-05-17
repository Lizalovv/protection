from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
PROTECTED_FOLDER = os.path.join(UPLOAD_FOLDER, 'protected')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROTECTED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    try:
        version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        version = str(e)
    return f'DexShield Server is running!<br><br><pre>{version}</pre>'

@app.route('/protect', methods=['POST'])
def protect():
    if 'apk' not in request.files:
        return jsonify({'error': 'No APK file provided'}), 400

    apk_file = request.files['apk']
    apk_filename = apk_file.filename
    apk_path = os.path.join(UPLOAD_FOLDER, apk_filename)
    apk_file.save(apk_path)

    java_bin = "java"
    jar_path = "dpt.jar"

    cmd = [java_bin, "-jar", jar_path, "-f", apk_path, "-o", PROTECTED_FOLDER]

    try:
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if process.returncode != 0:
            return jsonify({'error': process.stderr}), 500

        # Search for APK file in PROTECTED_FOLDER
        for file in os.listdir(PROTECTED_FOLDER):
            if file.endswith(".apk"):
                return send_file(os.path.join(PROTECTED_FOLDER, file), as_attachment=True)

        return jsonify({'error': 'Protected APK not found'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
