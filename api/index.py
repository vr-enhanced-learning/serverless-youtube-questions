from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from youtube_transcript_api import YouTubeTranscriptApi
import requests

def get_transcript(video_id):
    
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US'])    

    def array_fi(array):
        newArray = []
        for item in array:
            newArray.append(item["text"])
        return newArray
    return array_fi(srt)

def get_sentences(text, num_of_sentences=5):
    length = len(text)
    length_of_each_part = length // num_of_sentences
    new_array = []
    for i in range(0, 5):
        new_array.append(text[i*length_of_each_part:(i+1)*length_of_each_part])
    return new_array

def parse(array):
    text = ""
    for item in array:
        text += item
    return text

def print_array_as_sentences(array):
    for sentence in array:
        print(sentence)

def get_responses(array):
    questions_array = []
    for sentence in array:
        print("Generating Question " + str(array.index(sentence) + 1) + "...")
        sentence = parse(sentence)
        response = requests.post("https://currentlyexhausted-question-generator.hf.space/run/predict", json={
            "data": [
                sentence,
            ]
        }).json()
        questions_array.append(response["data"][0])
    return questions_array

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def api():
    if request.method == 'GET':
        return "It is working"

    data = request.get_json()
    youtube_video_id = data["youtubeVideoId"]
    sentences = get_transcript(youtube_video_id)
    array = get_sentences(sentences)

    questions = get_responses(array)
    return jsonify(questions)


if __name__ == '__main__':
    app.run(debug=True)