# Instruções para Executar o Código de Busca em PDF com LangChain

Este projeto realiza a busca em documentos PDF utilizando a biblioteca **LangChain** e o modelo de embeddings **Ollama**. O código carrega um arquivo PDF, divide o conteúdo em chunks, cria um banco de dados com os embeddings do texto e permite realizar buscas sobre o conteúdo do documento.

## Pré-requisitos

Antes de executar o código, você precisará garantir que algumas bibliotecas estão instaladas em seu ambiente Python.

### Instalação das Dependências

Para instalar as bibliotecas necessárias, você pode usar o `pip`. Execute os seguintes comandos para instalar os pacotes principais:

```bash
pip install langchain
pip install langchain_ollama
pip install faiss-cpu
Observação sobre FAISS:
Se você tem uma GPU e deseja usar o FAISS com aceleração por GPU, use o seguinte comando em vez do faiss-cpu:

bash
Copiar código
pip install faiss-gpu
Descrição do Código
1. Carregamento e Processamento de PDF
O código começa carregando o arquivo PDF utilizando o PyPDFLoader da biblioteca LangChain. Em seguida, o conteúdo é dividido em "chunks", ou pedaços de texto, usando o RecursiveCharacterTextSplitter para facilitar a busca e a análise.

python
Copiar código
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

pdf_path = 'Avaliacao5_TASI/cartilha.pdf'  # Caminho do PDF
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)

texts = text_splitter.split_documents(pages)
2. Construção do Banco de Dados com Embeddings
Após dividir o texto, o código gera embeddings usando o modelo OllamaEmbeddings e armazena essas representações em um banco de dados FAISS, que é uma estrutura eficiente para busca de similaridade.

python
Copiar código
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import FAISS

db = FAISS.from_documents(texts, OllamaEmbeddings(model="mxbai-embed-large"))
3. Consulta ao Banco de Dados
O código permite realizar uma busca no banco de dados, retornando os documentos mais relevantes (chunks) baseados na similaridade com a consulta fornecida pelo usuário.

python
Copiar código
from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA

model = OllamaLLM(model="llama3.2:latest")
retriever = db.as_retriever(search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever, chain_type="stuff")

query = input("\n**** Faça uma pergunta sobre códigos maliciosos: ")
response = qa_chain.invoke(query)
print("QA Response:", response["result"])
Passos para Executar
Passo 1: Instalar as Bibliotecas Necessárias
Abra o terminal ou prompt de comando e execute os seguintes comandos:

bash
Copiar código
pip install langchain
pip install langchain_ollama
pip install faiss-cpu  # ou faiss-gpu, se você estiver utilizando GPU
Passo 2: Carregar o Arquivo PDF
Certifique-se de que o caminho do arquivo PDF (pdf_path) esteja correto. O arquivo PDF será carregado e o seu conteúdo será dividido em chunks para análise posterior.

Passo 3: Rodar o Código
Após garantir que as dependências estão instaladas e o caminho do arquivo PDF está correto, execute o código Python.

O código irá carregar o PDF e dividi-lo em pedaços (chunks).
Você verá a quantidade de chunks gerados, além de um exemplo do conteúdo de um dos primeiros chunks.
Em seguida, o código criará um banco de dados FAISS com os embeddings dos textos.
Passo 4: Realizar uma Consulta
Quando o código pedir para você fazer uma pergunta, digite uma consulta sobre o tema contido no PDF (por exemplo, sobre códigos maliciosos, conforme o código sugere). O modelo irá buscar os chunks mais relevantes e apresentar a resposta.

Exemplo de Saída
bash
Copiar código
**** Faça uma pergunta sobre códigos maliciosos: O que é malware?
QA Response: O malware é um tipo de software malicioso projetado para danificar ou explorar qualquer dispositivo, serviço ou rede...
Observações Importantes
Certifique-se de que o arquivo PDF esteja no caminho correto. Caso contrário, o código retornará um erro.
O modelo Ollama utilizado no código pode exigir uma chave de API ou configuração adicional dependendo da sua conta. Consulte a documentação do Ollama caso tenha problemas para carregar o modelo.
O FAISS pode ser instalado com aceleração por GPU caso tenha suporte no seu ambiente, o que pode melhorar a velocidade de busca.