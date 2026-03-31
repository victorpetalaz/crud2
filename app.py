from flask import Flask, jsonify, request
# Importando a extensão do SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da URI do banco de dados (utilizando SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
# Desativa o rastreamento de modificações para economizar recursos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instanciando o banco de dados no app
db = SQLAlchemy(app)

# Definindo o modelo da tabela 'games'
class Game(db.Model):
    __tablename__ = 'games'
    
    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # Método para serializar o objeto (facilita o retorno em JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "platform": self.platform,
            "year": self.year
        }

@app.route('/games', methods=['GET'])
@app.route('/games/<int:id>', methods=['GET'])
def get_games(id=None):
    if id:
        # Busca um jogo específico pelo ID
        game = db.session.get(Game, id)
        if game:
            return jsonify(game.to_dict()), 200
        return jsonify({"error": "Not found :/"}), 404
    
    # Busca todos os jogos cadastrados
    games = db.session.execute(db.select(Game)).scalars().all()
    return jsonify([game.to_dict() for game in games]), 200


@app.route('/games', methods=['POST'])
def add_game():
    d = request.get_json()
    if not d or not all(k in d for k in ("title", "platform", "year")):
        return jsonify({"error ": "Missing data (title, platform, year required)"}), 400
    
    # Instancia um novo jogo com os dados recebidos
    new_game = Game(
        title=d['title'], 
        platform=d['platform'], 
        year=d['year']
    )
    
    # Adiciona e salva (commit) o novo registro no banco
    db.session.add(new_game)
    db.session.commit()
    
    return jsonify({"return!": "created :)"}), 201


@app.route('/games/<int:id>', methods=['PUT'])
def upd_game(id):
    d = request.get_json()
    if not d or not all(k in d for k in ("title", "platform", "year")):
        return jsonify({"error!": "missing data :/"}), 400

    # Busca o jogo para atualizar
    game = db.session.get(Game, id)
    if not game:
        return jsonify({"error!": "not found :/"}), 404

    # Atualiza os dados do objeto
    game.title = d['title']
    game.platform = d['platform']
    game.year = d['year']
    
    # Salva as alterações no banco
    db.session.commit()
    
    return '', 204


@app.route('/games/<int:id>', methods=['DELETE'])
def del_game(id):
    # Busca o jogo que será deletado
    game = db.session.get(Game, id)
    
    if not game:
        return jsonify({"error!": "not found :/"}), 404

    # Remove o objeto e salva no banco
    db.session.delete(game)
    db.session.commit()

    return jsonify({"return": "deleted!"}), 200


if __name__ == '__main__':
    # Cria as tabelas no banco de dados automaticamente, caso não existam
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)