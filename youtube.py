from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

def get_available_formats(youtube_url):
    try:
        yt = YouTube(youtube_url)
        formats = yt.streams.filter(progressive=True, file_extension='mp4')
        video_qualities = []
        audio_qualities = []

        for stream in formats:
            resolution = stream.resolution
            abr = stream.abr
            if resolution:
                video_qualities.append(resolution)
            if abr:
                audio_qualities.append(abr)

        return {'video': video_qualities, 'audio': audio_qualities}
    except Exception as e:
        return {'video': [], 'audio': []}

@app.route('/')
def index():
    return render_template('index.html', qualities=None)

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['url']
    selected_format = request.form['format']
    selected_quality = request.form['quality']

    try:
        yt = YouTube(youtube_url)
        if selected_format == 'video':
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_quality).first()
        else:
            stream = yt.streams.filter(only_audio=True, abr=selected_quality).first()
        if stream:
            stream.download()
            flash('Video downloaded successfully!', 'success')
        else:
            flash('Selected format/quality not available for this video.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/get_qualities', methods=['POST'])
def get_qualities():
    youtube_url = request.form['url']
    qualities = get_available_formats(youtube_url)
    return render_template('index.html', qualities=qualities)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

def get_available_formats(youtube_url):
    try:
        yt = YouTube(youtube_url)
        formats = yt.streams.filter(progressive=True, file_extension='mp4')
        video_qualities = set()
        audio_qualities = set()

        for stream in formats:
            resolution = stream.resolution
            abr = stream.abr
            if resolution:
                video_qualities.add(resolution)
            if abr:
                audio_qualities.add(abr)

        video_qualities = sorted(video_qualities, key=lambda x: int(x[:-1]))
        audio_qualities = sorted(audio_qualities)
        
        return {'video': video_qualities, 'audio': audio_qualities}
    except Exception as e:
        return {'video': [], 'audio': []}

@app.route('/')
def index():
    return render_template('index.html', qualities=None)

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['url']
    selected_format = request.form['format']
    selected_quality = request.form['quality']

    try:
        yt = YouTube(youtube_url)
        if selected_format == 'video':
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_quality).first()
        else:
            stream = yt.streams.filter(only_audio=True, abr=selected_quality).first()
        if stream:
            stream.download()
            flash('Video downloaded successfully!', 'success')
        else:
            flash('Selected format/quality not available for this video.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/get_qualities', methods=['POST'])
def get_qualities():
    youtube_url = request.form['url']
    qualities = get_available_formats(youtube_url)
    return render_template('index.html', qualities=qualities)

if __name__ == '__main__':
    app.run(debug=True)
