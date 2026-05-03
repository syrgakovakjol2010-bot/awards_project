from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

VOTES_FILE = '/tmp/votes.json' if os.environ.get('RENDER') else 'votes.json'

# Расширенная структура с поддержкой двух языков для заголовков
AWARDS_DATA = {
    "cis": {
        "streamer": {"ru": "Лучший Стример", "en": "Best Streamer", "icon": "🎮", "nominees": ["Buster", "Kuplinov", "Evelone192", "JesusAVGN", "Bratishkinoff", "Dmitry Lixxx", "Stray228"]},
        "youtuber": {"ru": "Лучший Ютубер", "en": "Best YouTuber", "icon": "🎥", "nominees": ["A4", "Дима Масленников", "Marmok", "HiMan", "Utopia Show", "Pryatki", "TheBrianMaps"]},
        "musician": {"ru": "Музыкант Года", "en": "Artist of the Year", "icon": "🎵", "nominees": ["Morgenshtern", "Slava Marlow", "Shadowraze", "Kizaru", "Big Baby Tape", "Instasamka", "Macan"]},
        "mobile": {"ru": "Mobile Автор", "en": "Mobile Creator", "icon": "📱", "nominees": ["Holdik", "AuRuM", "Злой", "Chizh", "Robzi", "IceArrow", "Pandora"]},
        "tech": {"ru": "Техноблогер", "en": "Tech Blogger", "icon": "💡", "nominees": ["Wylsacom", "808", "Rozetked", "Pro Hi-Tech", "Danya Master", "Чудо Техники"]},
        "discovery": {"ru": "Прорыв Года", "en": "Breakthrough", "icon": "🎭", "nominees": ["Koreshzy", "Paradeevich", "Frame Tamer", "Akyuliych", "Danila Gorilla", "VooDooSh"]}
    },
    "world": {
        "streamer": {"ru": "Мировой Стример", "en": "Global Streamer", "icon": "🌍", "nominees": ["xQc", "Kai Cenat", "Ibai", "Ninja", "Rubius", "Asmongold", "Speed"]},
        "youtuber": {"ru": "Мировой Ютубер", "en": "Global YouTuber", "icon": "🌐", "nominees": ["MrBeast", "PewDiePie", "Mark Rober", "Dude Perfect", "Sidemen", "Casey Neistat", "Ryan Trahan"]},
        "musician": {"ru": "Мировой Артист", "en": "World Artist", "icon": "🎸", "nominees": ["Drake", "The Weeknd", "Travis Scott", "Taylor Swift", "Post Malone", "Kanye West", "Eminem"]},
        "mobile": {"ru": "Mobile Эксперт", "en": "Mobile Expert", "icon": "📲", "nominees": ["Ferg", "Tribal", "OrangeJuice", "Powerbang", "Godzly", "Bobby Plays"]},
        "tech": {"ru": "Техно Гуру", "en": "Tech Guru", "icon": "💻", "nominees": ["Marques Brownlee", "Linus Tech Tips", "Unbox Therapy", "Mrwhosetheboss", "iJustine", "Dave2D"]},
        "discovery": {"ru": "Мировое Открытие", "en": "World Discovery", "icon": "✨", "nominees": ["IShowSpeed", "Sketch", "Jynxzi", "CaseOh", "Stable Ronaldo", "Baby OTT"]}
    }
}

def init_db():
    if not os.path.exists(VOTES_FILE):
        db = {"cis": {}, "world": {}}
        for reg in AWARDS_DATA:
            for cat, info in AWARDS_DATA[reg].items():
                db[reg][cat] = {name: 0 for name in info["nominees"]}
        with open(VOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

def load_db():
    init_db()
    with open(VOTES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    votes = load_db()
    leaders = {reg: {cat: max(votes[reg][cat], key=votes[reg][cat].get) if votes[reg][cat] else "" for cat in votes[reg]} for reg in ["cis", "world"]}
    return render_template('index.html', votes=votes, leaders=leaders, meta=AWARDS_DATA)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    reg, cat, name = data.get('reg'), data.get('cat'), data.get('name')
    db = load_db()
    if reg in db and cat in db[reg] and name in db[reg][cat]:
        db[reg][cat][name] += 1
        with open(VOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        return jsonify({"success": True, "count": db[reg][cat][name], "leader": max(db[reg][cat], key=db[reg][cat].get)})
    return jsonify({"success": False}), 400

if __name__ == '__main__':
    app.run(debug=True)
