from flask import Flask, Response, render_template
import os
#from get_image import get_image
#from get_video import get_video
#from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

@app.route('/')
def index():
    """ Route to serve the webpage """
    return render_template('index.html')  # You need to create this HTML file

def generate_video(video_path):
    """ Video streaming generator function """
    with open(video_path, 'rb') as video_file:
        while True:
            data = video_file.read(1024)
            if not data:
                break
            yield data

@app.route('/video/<video_name>')
def video(video_name):
    """ Route to stream video """
    video_path = os.path.join('.', video_name)  # Replace 'path_to_videos' with the folder containing your videos
    return Response(generate_video(video_path), mimetype='video/mp4')

if __name__ == '__main__':
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(get_image, 'interval', hours=6)
    #scheduler.add_job(get_video, 'interval', hours=6)
    #scheduler.start()
    app.run(debug=True)
