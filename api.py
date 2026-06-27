from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados pra teste
livros = [
    {"id": 1, "titulo": "Clean Code", "disponivel": True},
    {"id": 2, "titulo": "Design Patterns", "disponivel": False},
    {"id": 3, "titulo": "Introdução à Engenharia de Software", "disponivel": True},
    {"id": 4, "titulo": "UML", "disponivel": True},
    {"id": 5, "titulo": "Biblia de Java", "disponivel": True},
]


@app.route("/livros", methods=["GET"])
def listar_livros():
    """
    Retorna todos os livros ou filtra pelo título.
    """

    titulo = request.args.get("titulo")

    # Se nenhum título foi informado, retorna todos
    if titulo is None:
        return jsonify(livros)

    # Busca ignorando maiúsculas e minúsculas
    resultado = [
        livro
        for livro in livros
        if titulo.lower() in livro["titulo"].lower()
    ]

    return jsonify(resultado)


@app.route("/livros/<int:id>", methods=["GET"])
def buscar_por_id(id):
    """
    Retorna um livro pelo ID.
    """

    for livro in livros:
        if livro["id"] == id:
            return jsonify(livro)

    return jsonify({"erro": "Livro não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)