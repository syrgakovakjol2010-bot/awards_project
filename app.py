from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Используем папку /tmp для хранения файла, если мы на Render
if os.environ.get('RENDER'):
    VOTES_FILE = '/tmp/votes.json'
else:
    VOTES_FILE = 'votes.json'

def init_db():
    if not os.path.exists(VOTES_FILE):
        initial_data = {
            "cis": {
                "streamer": {"Buster": 0, "Kuplinov": 0, "Evelone192": 0, "JesusAVGN": 0, "Bratishkinoff": 0},
                "youtuber": {"A4": 0, "Дима Масленников": 0, "Marmok": 0, "HiMan": 0, "Utopia Show": 0}
            },
            "world": {
                "streamer": {"xQc": 0, "Kai Cenat": 0, "Ibai": 0, "Ninja": 0, "Rubius": 0},
                "youtuber": {"MrBeast": 0, "PewDiePie": 0, "Mark Rober": 0, "Dude Perfect": 0, "Sidemen": 0}
            }
        }
        with open(VOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)

def load_votes():
    init_db()  # Проверяем базу перед каждым чтением
    with open(VOTES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_votes(data):
    with open(VOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    try:
        votes = load_votes()
        return render_template('index.html', votes=votes)
    except Exception as e:
        return f"Произошла ошибка: {e}", 500

@app.route('/vote', methods=['POST'])
def vote():
    req_data = request.get_json()
    camp = req_data.get('camp')
    category = req_data.get('category')
    nominee = req_data.get('nominee')
    
    votes = load_votes()
    
    if camp in votes and category in votes[camp] and nominee in votes[camp][category]:
        votes[camp][category][nominee] += 1
        save_votes(votes)
        return jsonify({"success": True, "new_votes": votes[camp][category][nominee]})
        
    return jsonify({"success": False, "error": "Некорректные данные"}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
    
