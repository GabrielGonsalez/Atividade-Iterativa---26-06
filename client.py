import asyncio
import os

from dotenv import load_dotenv
from google import genai

from fastmcp import Client

load_dotenv()

MODEL = "gemini-2.5-flash"

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def escolher_ferramenta(pergunta: str):
    """
    Decide qual ferramenta MCP utilizar.
    Retorna (nome_da_ferramenta, argumentos)
    """

    texto = pergunta.lower()

    if "todos os livros" in texto or "listar" in texto or "disponíveis" in texto:
        return ("listar_livros", {})

    if "clean code" in texto:
        return ("buscar_livro", {"titulo": "Clean Code"})

    if "design patterns" in texto:
        return ("buscar_livro", {"titulo": "Design Patterns"})

    if "uml" in texto:
        return ("buscar_livro", {"titulo": "UML"})

    if "engenharia de software" in texto:
        return ("buscar_livro", {"titulo": "Introdução à Engenharia de Software"})

    if "java" in texto:
        return ("buscar_livro", {"titulo": "Biblia de Java"})

    return (None, None)


async def main():

    async with Client("mcp_server.py") as mcp:

        print("Assistente da Biblioteca")
        print("Digite 'sair' para encerrar.\n")

        while True:

            pergunta = input("Você: ")

            if pergunta.lower() == "sair":
                break

            ferramenta, argumentos = escolher_ferramenta(pergunta)

            contexto = ""

            if ferramenta:

                print(f"\n[MCP] Chamando ferramenta: {ferramenta}")

                resultado = await mcp.call_tool(
                    ferramenta,
                    argumentos
                )

                contexto = str(resultado)

            prompt = f"""
Você é um assistente de uma biblioteca.

Utilize as informações abaixo para responder.

Caso existam informações da biblioteca, responda SOMENTE utilizando essas informações.

Informações:

{contexto}

Pergunta:

{pergunta}
"""

            resposta = gemini.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            print("\nIA:")
            print(resposta.text)
            print()


if __name__ == "__main__":
    asyncio.run(main())