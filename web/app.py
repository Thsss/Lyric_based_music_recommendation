from flask import Flask, jsonify, request
from flask_cors import cross_origin
from model import *

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/search/', methods=['GET'])
@cross_origin()
def search():
    content = request.args.get('content')
    sim_songs = recom_music(lyrics, train_corpus, model, content)
    data = []
    for i in range(len(sim_songs)):
        item = {}
        item['song'] = sim_songs[i][0]
        item['singer'] = sim_songs[i][1]
        item['sim'] = "{:.3f}".format(sim_songs[i][2])
        item['web'] = "music.163.com/#/search/m/?s={}".format(sim_songs[i][0])
        data.append(item)

    # data = [
    #     {'song': '{}'.format(content), 'singer': '1', 'sim': 0.99, 'web': ''},
    #     {'song': 'B', 'singer': '2', 'sim': 0.99, 'web': 'music.163.com/#/search/m/?s=不得不爱'},
    #     {'song': 'C', 'singer': '3', 'sim': 0.99, 'web': 'music.163.com/#/search/m/?s=不得不爱'},
    #     {'song': 'D', 'singer': '4', 'sim': 0.99, 'web': 'music.163.com/#/search/m/?s=不得不爱'},
    #     {'song': 'E', 'singer': '5', 'sim': 0.99, 'web': 'music.163.com/#/search/m/?s=不得不爱'},
    #     {'song': 'F', 'singer': '6', 'sim': 0.99, 'web': 'music.163.com/#/search/m/?s=不得不爱'},
    # ]
    return jsonify(data)


if __name__ == '__main__':
    lyrics, train_corpus, model = load()
    app.run()
