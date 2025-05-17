from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    try:
        version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        version = str(e)
    return f'DexShield Server is running!<br><br><pre>{version}</pre>'


from flask import send_file

@app.route('/protect', methods=['POST'])
def protect():
    if 'apk' not in request.files:
        return jsonify({'error': 'No APK file provided'}), 400
    
    apk_file = request.files['apk']
    apk_path = os.path.join(UPLOAD_FOLDER, apk_file.filename)
    apk_file.save(apk_path)

    java_bin = "java"
    jar_path = "dpt.jar"

    output_dir = os.path.join(UPLOAD_FOLDER, "protected")
    os.makedirs(output_dir, exist_ok=True)

    cmd = [java_bin, "-jar", jar_path, "-f", apk_path, "-o", output_dir]

    try:
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if process.returncode != 0:
            return jsonify({'error': process.stderr}), 500
        else:
            # Assume output APK has same filename in output_dir
            protected_apk_path = os.path.join(output_dir, apk_file.filename)
            if os.path.exists(protected_apk_path):
                return send_file(protected_apk_path, as_attachment=True)
            else:
                return jsonify({'error': 'Protected APK not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
