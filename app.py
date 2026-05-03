from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к базе данных (совместимо с Render)
VOTES_FILE = '/tmp/votes.json' if os.environ.get('RENDER') else 'votes.json'

# Полная структура всех наград и номинантов
AWARDS_DATA = {
    "cis": {
        "streamer": {"title": "Лучший Стример", "icon": "🎮", "nominees": ["Buster", "Kuplinov", "Evelone192", "JesusAVGN", "Bratishkinoff", "Dmitry Lixxx", "Stray228"]},
        "youtuber": {"title": "Лучший Ютубер", "icon": "🎥", "nominees": ["A4", "Дима Масленников", "Marmok", "HiMan", "Utopia Show", "Pryatki", "TheBrianMaps"]},
        "musician": {"title": "Музыкант Года", "icon": "🎵", "nominees": ["Morgenshtern", "Slava Marlow", "Shadowraze", "Kizaru", "Big Baby Tape", "Instasamka", "Macan"]},
        "mobile": {"title": "Mobile Автор", "icon": "📱", "nominees": ["Holdik", "AuRuM", "Злой", "Chizh", "Robzi", "IceArrow", "Pandora"]},
        "tech": {"title": "Техноблогер", "icon": "💡", "nominees": ["Wylsacom", "808", "Rozetked", "Pro Hi-Tech", "Danya Master", "Чудо Техники"]},
        "discovery": {"title": "Прорыв Года", "icon": "🎭", "nominees": ["Koreshzy", "Paradeevich", "Frame Tamer", "Akyuliych", "Danila Gorilla", "VooDooSh"]}
    },
    "world": {
        "streamer": {"title": "Global Streamer", "icon": "🌍", "nominees": ["xQc", "Kai Cenat", "Ibai", "Ninja", "Rubius", "Asmongold", "Speed"]},
        "youtuber": {"title": "Global YouTuber", "icon": "🌐", "nominees": ["MrBeast", "PewDiePie", "Mark Rober", "Dude Perfect", "Sidemen", "Casey Neistat", "Ryan Trahan"]},
        "musician": {"title": "World Artist", "icon": "🎸", "nominees": ["Drake", "The Weeknd", "Travis Scott", "Taylor Swift", "Post Malone", "Kanye West", "Eminem"]},
        "mobile": {"title": "Mobile Creator", "icon": "📲", "nominees": ["Ferg", "Tribal", "OrangeJuice", "Powerbang", "Godzly", "Bobby Plays"]},
        "tech": {"title": "Tech Guru", "icon": "💻", "nominees": ["Marques Brownlee", "Linus Tech Tips", "Unbox Therapy", "Mrwhosetheboss", "iJustine", "Dave2D"]},
        "discovery": {"title": "World Discovery", "icon": "✨", "nominees": ["IShowSpeed", "Sketch", "Jynxzi", "CaseOh", "Stable Ronaldo", "Baby OTT"]}
    }
}

def init_db():
    if not os.path.exists(VOTES_FILE):
        db = {"cis": {}, "world": {}}
        for region in AWARDS_DATA:
            for cat, info in AWARDS_DATA[region].items():
                db[region][cat] = {name: 0 for name in info["nominees"]}
        with open(VOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

def load_db():
    init_db()
    with open(VOTES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(VOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    votes = load_db()
    leaders = {"cis": {}, "world": {}}
    for reg in ["cis", "world"]:
        for cat in votes[reg]:
            leaders[reg][cat] = max(votes[reg][cat], key=votes[reg][cat].get) if votes[reg][cat] else ""
    return render_template('index.html', votes=votes, leaders=leaders, meta=AWARDS_DATA)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    reg, cat, name = data.get('reg'), data.get('cat'), data.get('name')
    db = load_db()
    if reg in db and cat in db[reg] and name in db[reg][cat]:
        db[reg][cat][name] += 1
        save_db(db)
        new_leader = max(db[reg][cat], key=db[reg][cat].get)
        return jsonify({"success": True, "count": db[reg][cat][name], "leader": new_leader})
    return jsonify({"success": False}), 400

if __name__ == '__main__':
    app.run(debug=True)
