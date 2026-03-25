from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def exec_q(q, *args, fetch=False, commit=False):
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    res = None
    
    try:
        c.execute(q, args)
        if commit:
            conn.commit()
        if fetch:
            res = c.fetchall()
    finally:
        conn.close()
    
    return res

@app.route('/games', methods=['GET'])
@app.route('/games/<int:id>', methods=['GET'])
def get_games(id=None):
    if id:
        game = exec_q("SELECT * FROM games WHERE id = ?", id, fetch=True)
        if game:
            return jsonify(dict(game[0])), 200
        return jsonify({"err": "Not found"}), 404

    data = exec_q("SELECT * FROM games", fetch=True)
    return jsonify([dict(i) for i in data]), 200

@app.route('/games', methods=['POST'])
def add_game():
    d = request.get_json()
    exec_q(
        "INSERT INTO games (title, plat, yr) VALUES (?, ?, ?)",
        d.get('title'), d.get('plat'), d.get('yr'),
        commit=True
    )
    return jsonify({"msg": "Created"}), 201

@app.route('/games/<int:id>', methods=['PUT'])
def upd_game(id):
    d = request.get_json()
    
    exists = exec_q("SELECT id FROM games WHERE id = ?", id, fetch=True)
    if not exists:
        return jsonify({"err": "Not found"}), 404

    exec_q(
        "UPDATE games SET title = ?, plat = ?, yr = ? WHERE id = ?",
        d.get('title'), d.get('plat'), d.get('yr'), id,
        commit=True
    )
    return '', 204

@app.route('/games/<int:id>', methods=['DELETE'])
def del_game(id):
    exists = exec_q("SELECT id FROM games WHERE id = ?", id, fetch=True)
    if not exists:
        return jsonify({"err": "Not found"}), 404

    exec_q("DELETE FROM games WHERE id = ?", id, commit=True)
    return jsonify({"msg": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)