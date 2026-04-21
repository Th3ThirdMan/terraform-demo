from flask import Flask, jsonify, request
import sqlite3

import sqlite3

def get_db():
    conn = sqlite3.connect('notes.db')
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
    return """
<h1>📝 Notes App</h1>
<form id="noteForm">
    <input type="text" id="noteInput" placeholder="Write a note..." />
    <button type="submit">Add</button>
</form>

<ul id="notesList"></ul>

<script>
async function loadNotes() {
    const res = await fetch('/notes');
    const data = await res.json();

    const list = document.getElementById('notesList');
    list.innerHTML = '';

    data.notes.forEach(n => {
        const li = document.createElement('li');
        li.textContent = n.text;
        list.appendChild(li);
    });
}

document.getElementById('noteForm').onsubmit = async (e) => {
    e.preventDefault();

    const input = document.getElementById('noteInput');
    const text = input.value;

    await fetch('/notes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text })
    });

    input.value = '';
    loadNotes();
};

loadNotes();
</script>
"""


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