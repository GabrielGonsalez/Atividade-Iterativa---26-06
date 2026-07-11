# Atividade-Iterativa---26-06

# Assistente Inteligente para Biblioteca

Este projeto foi desenvolvido como parte da atividade da disciplina de **Redes de Computadores** e tem como objetivo demonstrar de forma prática, a utilização dos protocolos Model Context Protocol (MCP) e HTTP em uma aplicação simples baseada em Inteligência Artificial.

O sistema simula um Assistente Inteligente para Biblioteca, permitindo que um usuário faça consultas em linguagem natural, como:

- "Quais livros estão disponíveis?"
- "O livro Clean Code está disponível?"

Para interpretar as solicitações do usuário, o projeto utiliza uma **LLM (Large Language Model)**, como o **Gemini**, conectada a um **servidor MCP**. O modelo de IA é responsável por compreender a pergunta do usuário e decidir quando utilizar uma ferramenta disponibilizada pelo servidor MCP.

O **MCP** é o protocolo principal da aplicação, permitindo que a IA interaja com ferramentas externas de forma padronizada. 

As ferramentas implementadas no servidor MCP não acessam diretamente os dados da biblioteca; em vez disso, realizam requisições **HTTP** para uma pequena API desenvolvida em **Flask**.

A API Flask representa o sistema da biblioteca e disponibiliza informações sobre os livros por meio de endpoints REST. Dessa forma, o projeto evidencia a integração entre os dois protocolos:

- **MCP**, responsável pela comunicação entre a LLM e as ferramentas disponíveis;
- **HTTP**, utilizado pelas ferramentas do MCP para consumir os serviços oferecidos pela API da biblioteca.

## O fluxo da aplicação é:

```
Usuário
    V
LLM (Gemini)
    V
Servidor MCP
    V
Requisição HTTP
    V
API Flask
    V
Resposta
    V
LLM
    V
Usuário
```

## Estrutura da aplicação

| Arquivo | Função |
|---------|---------|
| `api.py` | Implementa a API REST da biblioteca utilizando Flask. |
| `mcp_server.py` | Implementa o servidor MCP e define as ferramentas utilizadas pela LLM. |
| `client.py` | Conecta o Gemini ao servidor MCP e permite a interação do usuário. |
| `requirements.txt` | Lista as dependências necessárias para executar o projeto. |
| `.env` | Armazena de forma discreta a chave da API do Gemini e outras configurações sensíveis para evitar possiveis problemas de segurança. |
| `README.md` | Documentação do projeto e instruções de execução. |


## Como executar

### 1. Instale as dependências

```
pip install -r requirements.txt
```

### 2. Configure sua chave API Gemini (ou qualquer LLM de sua preferência) 

```
GEMINI_API_KEY=(sua_chave_aqui)
```

### 3. Inicie a API flask

Abra um terminal e execute:
```
python api.py
```

### 4. Inicie o servidor MCP
Enquanto a api estiver rodando, abra outro terminal e execute:
```
python mcp_server.py
```

### 5. Inicie o client 
Abra um terceiro terminal e execute:
```
python client.py
```