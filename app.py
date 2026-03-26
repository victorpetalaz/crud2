from flask import Flask, jsonify, request
from init_db import exec_q, init_db

app = Flask(__name__)

@app.route('/games', methods=['GET'])
@app.route('/games/<int:id>', methods=['GET'])
def get_games(id=None):
    if id:
        game = exec_q("SELECT * FROM games WHERE id = ?", id, fetch=True)
        if game:
            return jsonify(dict(game[0])), 200
        return jsonify({"error": "Not found :/"}), 404
    data = exec_q("SELECT * FROM games", fetch=True)
    return jsonify([dict(i) for i in data]), 200

@app.route('/games', methods=['POST'])
def add_game():
    d = request.get_json()
    if not d or not all(k in d for k in ("title", "platform", "year")):
        return jsonify({"error ": "Missing data (title, platform, year required)"}), 400
    exec_q(
        "INSERT INTO games (title, platform, year) VALUES (?, ?, ?)",
        d['title'], d['platform'], d['year'],
        commit=True
    )
    return jsonify({"return!": "created :)"}), 201

@app.route('/games/<int:id>', methods=['PUT'])
def upd_game(id):
    d = request.get_json()
    if not d or not all(k in d for k in ("title", "platform", "year")):
        return jsonify({"error!": "missing data :/"}), 400

    affected_rows = exec_q(
        "UPDATE games SET title = ?, platform = ?, year = ? WHERE id = ?",
        d['title'], d['platform'], d['year'], id,
        commit=True
    )
    
    if affected_rows == 0:
        return jsonify({"error!": "not found :/"}), 404
    return '', 204

@app.route('/games/<int:id>', methods=['DELETE'])
def del_game(id):
    affected_rows = exec_q("DELETE FROM games WHERE id = ?", id, commit=True)
    
    if affected_rows == 0:
        return jsonify({"error!": "not found :/"}), 404

    return jsonify({"return": "deleted!"}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
