from fastmcp import FastMCP
import requests

mcp = FastMCP("Biblioteca")

@mcp.tool()
def listar_livros():
    """
    Lista todos os livros cadastrados na biblioteca, incluindo ID, título e status de disponibilidade.
    """
    resposta = requests.get("http://localhost:5000/livros")
    resposta.raise_for_status()
    return resposta.json()

@mcp.tool()
def buscar_livro(titulo: str):
    """
    Busca livros na biblioteca que contenham o termo ou título informado.
    """
    resposta = requests.get(
        "http://localhost:5000/livros",
        params={"titulo": titulo}
    )
    resposta.raise_for_status()
    return resposta.json()

@mcp.tool()
def consultar_livro(id: int):
    """
    Consulta os detalhes de um livro específico utilizando o seu ID numérico.
    """
    resposta = requests.get(f"http://localhost:5000/livros/{id}")
    resposta.raise_for_status()
    return resposta.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")