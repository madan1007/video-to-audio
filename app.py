from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)

# Directories for uploads and converted files
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save the uploaded video
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)
    
    # Convert video to audio
    audio_filename = os.path.splitext(file.filename)[0] + '.mp3'
    audio_path = os.path.join(CONVERTED_FOLDER, audio_filename)
    
    try:
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"audioUrl": f"/converted/{audio_filename}"}), 200

@app.route('/converted/<filename>')
def serve_audio(filename):
    return send_from_directory(CONVERTED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
