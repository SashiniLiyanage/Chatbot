import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_pdf_text(pdf_docs):
    text = ""
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


def handle_userinput(user_question):

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.markdown(message.content)
        else:
            with st.chat_message("assistant"):
                st.markdown(message.content)
    
    with st.chat_message("user"):
                st.markdown(user_question)
    # with st.chat_message("assistant"):
    #             st.markdown("Typing...")
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            st.markdown(st.session_state.chat_history[-1].content)

def create_conversation(pdf_docs):
    # get pdf text
    raw_text = "My Name is Marshall Chatbot"
    if pdf_docs:
        raw_text = get_pdf_text(pdf_docs)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    # create conversation chain
    st.session_state.conversation = get_conversation_chain(vectorstore)

def main():
    load_dotenv()
    st.set_page_config(page_title="Marshall Chatbot", page_icon=":robot_face:")
    st.write(unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
        create_conversation(None)

    st.header("Marshall Chatbot :robot_face:")
    user_question = st.chat_input("What do you want to know about Marshall?")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Marshall documents")
        pdf_docs = st.file_uploader(
            "Upload the PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                create_conversation(pdf_docs)

if __name__ == '__main__':
    main()