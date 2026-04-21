from flask import Flask, jsonify, request, render_template
import sqlite3

import sqlite3

def get_db():
    conn = sqlite3.connect('/data/notes.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)

rows = get_db().execute("SELECT * FROM notes").fetchall()
return jsonify([dict(r) for r in rows])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
   

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify({'notes': notes})

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note = {
        'id': len(notes) + 1,
        'text': data.get('text')
    }
    notes.append(note)
    return jsonify(note)

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n['id'] != note_id]
    return jsonify({"deleted": note_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)