from flask import Flask, redirect, url_for, request,render_template
from utils import get_text, rag_pipeline
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def open_url(url):
    get_text.download(url,"downloaded","video")
    get_text.audio_from_video("video/downloaded.mp4",'saved_audio')
    get_text.get_text_from_audio('audio/saved_audio.wav','saved_text')
    res = rag_pipeline.get_result("text_output/saved_text.txt")
    print(res)
    return res

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        url = request.form['nm']
        data = open_url(url)
        return render_template('output.html', dataToRender=data)

    else:
        url = request.form['nm']
        data = open_url(url)
        return render_template('output.html', dataToRender=data)

if __name__ == '__main__':
    app.run(debug=True)