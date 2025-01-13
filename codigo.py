# Importação necessaria para trabalhar com arquivos PDFs
from langchain.document_loaders import PyPDFLoader
# Esta importação serve para quebrar o texto em chunks seguindo alguns parametros
from langchain.text_splitter import RecursiveCharacterTextSplitter

pdf_path = 'Avaliacao5_TASI/cartilha.pdf' # Arquivo que será ultilizado para futura busca
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

# parametros que será usado para criar chunks
text_splitter = RecursiveCharacterTextSplitter(
    #chunk_size=200,
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)

texts = text_splitter.split_documents(pages)

print(texts[0]) # imprimirar a primera pagina 

print (f"Quantidade de chunks: {len(texts)} ") # imprimirar a quantidade de paginas

# Antes de usar o FAISS devesse instala-lo, caso você posssuia GPU ultilize o seguinte codigo: pip install faiss-gpu
# Mas se preferir executar no CPU mesmo use o seguinte codigo: pip install faiss-cpu

from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import FAISS

db = FAISS.from_documents(texts,  OllamaEmbeddings(model="mxbai-embed-large")) # gerando um banco de dados com e embeddings do texto que anteriomente foi quebrado em thunks

# query = "o que é malware? " 

# Este codigo busca as duas thunks com maior similaridade da pergunta e exibira em seguida
# docs = db.similarity_search(query, k=2)
# for i, doc in enumerate(docs):
#    print(f"\nChunk {i + 1}: {doc.page_content}")

from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA
# Create the LLM model and retriever
model = OllamaLLM(model="llama3.2:latest")

# recuperando o retriever com 5 documentos
retriever = db.as_retriever(search_kwargs={"k": 5})
#retriever = db.as_retriever()

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever, chain_type="stuff")  
# Example usage of the RetrievalQA chain
query = input("\n**** Faça uma pergunda sobre codigos maliciosos: ") # permite que o usario faça uma busca sobre o tema que está na base de dados
response = qa_chain.invoke(query)
print("QA Response:", response["result"])