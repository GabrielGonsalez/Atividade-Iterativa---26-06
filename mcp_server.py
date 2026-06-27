from fastmcp import FastMCP
import requests

mcp = FastMCP("Biblioteca")

@mcp.tool()
def listar_livros():
    """Lista todos os livros."""

    resposta = requests.get("http://localhost:5000/livros")
    resposta.raise_for_status()

    return resposta.json()

@mcp.tool()
def buscar_livro(titulo: str):
    """Busca um livro pelo título."""

    resposta = requests.get(
        "http://localhost:5000/livros",
        params={"titulo": titulo}
    )
    resposta.raise_for_status()

    return resposta.json()

@mcp.tool()
def consultar_livro(id: int):
    """Consulta um livro pelo ID."""

    resposta = requests.get(
        f"http://localhost:5000/livros/{id}"
    )
    resposta.raise_for_status()

    return resposta.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")