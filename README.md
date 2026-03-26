# Games API 

API RESTful simples para gerenciar um inventário de jogos usando Flask e SQLite.

## Setup e Inicialização

Antes de testar a API, instale as dependências e o servidor:

  No terminal do VSCode:
pip install flask
python init_db.py
python app.py

    Roteiro de Testes (cURL)
    Execute os comandos abaixo em um novo terminal enquanto o app.py estiver rodando no terminal principal.
    1. POST (Inserir)
    O que é: Envia dados no formato JSON no corpo da requisição para a rota principal.

    Por que usar: Para salvar um novo registro no banco (Retorna status 201).
        curl -X POST http://127.0.0.1:5000/games -H "Content-Type: application/json" -d "{\"title\": \"Bloodborne\", \"platform\": \"PS4\", \"year\": 2015}"

    2. GET (Listar Todos)
    O que é: Faz uma requisição de leitura padrão para a rota principal.
    Por que usar: Para retornar uma lista JSON de todos os registros.
        curl http://127.0.0.1:5000/games
    
    3. GET (Buscar por ID)
    O que é: Faz uma requisição de leitura passando um parâmetro dinâmico na URL (/1).
    Por que usar: Para retornar apenas um registro específico (ou erro 404 se não existir).
        curl http://127.0.0.1:5000/games/1
    ou  curl http://127.0.0.1:5000/games/2
    
    4. PUT (Atualizar)
    O que é: Envia um novo JSON (payload) para a URL específica de um ID existente.
    Por que usar: Para alterar dados de um registro existente via ID (Retorna status 204).
        curl -X PUT http://127.0.0.1:5000/games/1 -H "Content-Type: application/json" -d "{\"title\": \"Bloodborne GOTY\", \"platform\": \"PS4\", \"year\": 2015}"
    
    5. DELETE (Remover)
    O que é: Envia um método de exclusão para a URL de um ID específico.
    Por que usar: Para excluir um registro do banco via ID.
        curl -X DELETE http://127.0.0.1:5000/games/1
