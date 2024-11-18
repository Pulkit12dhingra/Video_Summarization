# Load text File
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import google.generativeai as genai
genai.configure(api_key="") # put your own api key

# Text splitter
# usually done to break down large chunks of text into small ones 
# but gemini has good token size
from langchain.text_splitter import CharacterTextSplitter

# load document
def load_document(text_file):
    
    loader = TextLoader(text_file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    return docs

# get embeddings and vector store
def embedding_loader(text_file):
    
    doc = load_document(text_file)
    # Generate embeddings using Hugging Face
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    hf_embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    docs = load_document(text_file)
    vector_store = FAISS.from_documents(docs, hf_embeddings)

    return vector_store


# 5. Define a custom retriever function
def custom_retriever(query,vector_store):
    
    # Use FAISS to retrieve relevant documents based on the query
    retriever = vector_store.as_retriever()
    docs = retriever.get_relevant_documents(query)
    
    # Extract text from the retrieved documents
    retrieved_text = " ".join([doc.page_content for doc in docs])
    
    return retrieved_text

# 6. Query the model using Google's text generation function
def run_query(query,model,vector_store):
    # Retrieve relevant documents
    retrieved_text = custom_retriever(query,vector_store)
    
    response = model.generate_content(
        query + "\nContext:\n" + retrieved_text
    )
    
    
    # Return the generated text from the response
    return response.text  # Or response.generations[0].text if multiple generations are supported


def gemini_model():
    # 4. Create the Google Gemini model with generation config
    generation_config = {
        "temperature": 1,
        "top_p": 0.96,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    # Create the Gemini model (Google Generative AI)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Specify the Gemini model name
        generation_config=generation_config
    )
    return model

def get_result(text_file):
    # 7. Run a query
    model = gemini_model()
    vector_store = embedding_loader(text_file)
    query = "Summarize the document"
    result = run_query(query,model,vector_store)

    return result