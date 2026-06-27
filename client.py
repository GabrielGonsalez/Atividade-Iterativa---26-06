import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from fastmcp import Client

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"

async def main():

    async with Client("mcp_server.py") as mcp:

        print("Assistente da Biblioteca")
        print("Digite 'sair' para encerrar.\n")

        while True:

            pergunta = input("Você: ")

            if pergunta.lower() == "sair":
                break

            resposta = await client.aio.models.generate_content(
                model=MODEL,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    tools=[mcp]
                )
            )

            print("\nIA:", resposta.text)
            print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())