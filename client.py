import asyncio
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastmcp import Client

load_dotenv()

MODEL = "gemini-2.5-flash"
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def main():
    # Conecta ao servidor MCP
    async with Client("mcp_server.py") as mcp:
        print("Assistente da Biblioteca")
        print("Digite 'sair' para encerrar.\n")

        # Obtem a lista de ferramentas disponíveis no servidor MCP para mostrar ao modelo se necessário
        ferramentas_disponiveis = await mcp.list_tools()
        tools_info = "\n".join([f"- {t.name}: {t.description}" for t in ferramentas_disponiveis])

        while True:
            pergunta = input("Você: ")

            if pergunta.lower() == "sair":
                break

            # é pedido ao Gemini para decidir qual ferramenta usar com base na lista 
            prompt_orquestrador = f"""
            Com base na pergunta do usuário e nas ferramentas MCP disponíveis, decida se alguma ferramenta precisa ser chamada.
            
            Ferramentas disponíveis:
            {tools_info}
            
            Responda ESTRUTURADAMENTE em formato JSON (e NADA mais):
            {{
                "com_ferramenta": true/false,
                "nome_ferramenta": "nome_da_ferramenta_ou_null",
                "argumentos": {{ "nome_do_parametro": "valor" }} ou {{}}
            }}
            
            Pergunta do usuário: "{pergunta}"
            """

            try:
                # a resposta é forçada para o formato JSON para o orquestrador
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
                
                resposta_orquestrador = gemini.models.generate_content(
                    model=MODEL,
                    contents=prompt_orquestrador,
                    config=config
                )
                
                decisao = json.loads(resposta_orquestrador.text)
            except Exception as e:
                print(f"[Erro ao decodificar decisão da IA]: {e}")
                decisao = {"com_ferramenta": False}

            contexto = "Nenhuma informação extra obtida."

            if decisao.get("com_ferramenta") and decisao.get("nome_ferramenta"):
                ferramenta = decisao["nome_ferramenta"]
                argumentos = decisao.get("argumentos", {})
                
                print(f"\n[MCP] IA decidiu chamar: {ferramenta} com {argumentos}")
                
                try:
                    resultado = await mcp.call_tool(ferramenta, argumentos)
                    contexto = str(resultado)
                except Exception as e:
                    contexto = f"Erro ao executar a ferramenta {ferramenta}: {str(e)}"

            prompt_final = f"""
Você é um assistente de uma biblioteca.

Utilize as informações abaixo para responder.

Caso existam informações da biblioteca, responda SOMENTE utilizando essas informações.

Informações:

{contexto}

Pergunta:

{pergunta}
"""
            resposta_final = gemini.models.generate_content(
                model=MODEL,
                contents=prompt_final
            )

            print("\nIA:")
            print(resposta_final.text)
            print("-")

if __name__ == "__main__":
    asyncio.run(main())