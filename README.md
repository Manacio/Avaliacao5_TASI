Instruções para Executar o Código de Busca em PDF com LangChain
Este documento tem como objetivo explicar como configurar o ambiente e executar o código Python que realiza a busca em documentos PDF, utilizando a biblioteca LangChain juntamente com o modelo de embeddings Ollama. O código carrega um arquivo PDF, divide o conteúdo em chunks, cria um banco de dados com os embeddings do texto, e permite realizar buscas sobre o conteúdo do documento.

Pré-requisitos
Antes de executar o código, você precisará garantir que algumas bibliotecas estão instaladas em seu ambiente Python.

Instalação das Dependências
Para instalar as bibliotecas necessárias, você pode usar o pip. Execute os seguintes comandos para instalar os pacotes principais:
``` bash
pip install langchain
pip install langchain_ollama
pip install faiss-cpu
```