from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__, template_folder='templates')

def get_db():
    conn = sqlite3.connect('/data/notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = get_db()
    rows = conn.execute("SELECT * FROM notes").fetchall()
    notes = [dict(r) for r in rows]
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    text = data.get('text')

    if not text or not text.strip():
        return jsonify({'error': 'Text required'}), 400

    conn = get_db()
    cur = conn.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()

    return jsonify({'id': cur.lastrowid, 'text': text})

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()

    return jsonify({"deleted": note_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)