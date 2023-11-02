
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__)
load_dotenv()
CORS(app,resources={r"/*": {"origins": "http://localhost:8080"}})

@app.route('/list_files', methods=['GET'])
def list_files():
    file_names = [filename for filename in os.listdir(os.getenv('UPLOAD_FOLDER')) if filename.endswith(".pdf")]
    return jsonify(file_names), 200

@app.route('/delete_files', methods=['POST'])
def delete_files():
    if request.is_json:
        data = request.get_json()
        if "fileName" in data:
            fileName = data["fileName"]
            file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), fileName)
            if os.path.exists(file_path):
                os.remove(file_path)
                return jsonify({'message': f'File {fileName} has been removed.'}), 200
            else:
                return jsonify({'error': f'File {fileName} does not exist.'}), 404

        return jsonify({'error': 'Invalid request'}), 400


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'pdfs' not in request.files:
        return 'No PDFs provided', 400

    pdf_files = request.files.getlist('pdfs')
    uploaded_files = []

    for pdf in pdf_files:
        if pdf and pdf.filename.endswith('.pdf'):
            filename = os.path.join(os.getenv('UPLOAD_FOLDER'), pdf.filename)
            pdf.save(filename)
            uploaded_files.append(pdf.filename)

    return 'Uploaded PDFs: ' + ', '.join(uploaded_files), 200


@app.route('/process', methods=['POST'])
def process_files():
    create_conversation(os.getenv('UPLOAD_FOLDER'))
    return 'Successfuly Prcossed', 200


@app.route('/ask', methods=['POST'])
def handle_userinput():
    global conversation_chain
    if request.is_json:
        data = request.get_json()
        if "ques" in data:
            try:
                response = conversation_chain({'question': data["ques"]})
                chat_history = response['chat_history']
                return jsonify({"message":chat_history[-1].content}), 200
            
            except BaseException as e:
                return jsonify({"message":"Something went wrong! Please try again later."}), 200
            
        else:
            return 'No ques', 400

def get_pdf_text(pdf_path):
    text = "My Name is Marshall Chatbot."

    pdf_docs = [os.path.join(pdf_path, filename) for filename in os.listdir(pdf_path) if filename.endswith(".pdf")]
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def create_conversation(pdf_path):
    # get pdf text
    raw_text = "My Name is Marshall Chatbot"
    if pdf_path:
        raw_text = get_pdf_text(pdf_path)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    global conversation_chain
    conversation_chain = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    os.makedirs(os.getenv('UPLOAD_FOLDER'), exist_ok=True)
    conversation_chain = None
    create_conversation(os.getenv('UPLOAD_FOLDER'))
    app.run(debug=True)