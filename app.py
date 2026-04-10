from flask import Flask, render_template, request, url_for
import requests
from gtts import gTTS

app = Flask(__name__)

# 🔑 Your API Key
API_KEY = "AIzaSyAJ-3tFc3em8mzt9vG90C6Fyacrz1GqQUs"

# 🌍 Language codes
lang_map = {
    "english": "en",
    "telugu": "te",
    "hindi": "hi"
}

# 🎥 Smart YouTube fetch with filtering
def get_youtube_videos(query, topic):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=10&key={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    videos = []

    # 🔥 Topic keywords
    topic_keywords = {
        "data structures": ["data structure", "dsa", "algorithm"],
        "python": ["python"],
        "java": ["java"],
        "c": ["c programming", "c language"],
        "physics": ["physics"],
        "chemistry": ["chemistry"],
        "algebra": ["algebra", "math"]
    }

    keywords = topic_keywords.get(topic.lower(), [topic.lower()])

    for item in data.get('items', []):
        title = item['snippet']['title'].lower()
        video_id = item['id']['videoId']

        # 🔥 Check ANY keyword match
        if any(keyword in title for keyword in keywords):
            videos.append(f"https://www.youtube.com/watch?v={video_id}")

    # ⚠️ fallback (still filtered)
    if not videos:
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            videos.append(f"https://www.youtube.com/watch?v={video_id}")

    # 🔥 final fallback
    if not videos:
        videos = ["https://www.youtube.com/watch?v=_uQrJ0TkZlc"]

    return videos[:5]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    topic = request.form['topic']
    level = request.form['level']
    language = request.form['language']

    lang_code = lang_map.get(language, "en")

    # 🔍 Better query
    search_query = f"{topic} tutorial {level} {language} programming"

    videos = get_youtube_videos(search_query, topic)
    video = videos[0]

    # 🧠 Explanation
    if language == "telugu":
        explanation = f"{topic} గురించి సులభంగా అర్థమయ్యే విధంగా వివరణ."
    elif language == "hindi":
        explanation = f"{topic} को आसान तरीके से समझाया गया है।"
    else:
        explanation = f"{topic} explained clearly for better understanding."

    # 🔊 Voice
    tts = gTTS(text=explanation, lang=lang_code)
    tts.save("static/output.mp3")

    return render_template('result.html',
                           topic=topic,
                           explanation=explanation,
                           video=video,
                           videos=videos[1:],
                           lang_code=lang_code)


if __name__ == '__main__':
    app.run(debug=True)