from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ---------- Text Splitter ----------

def split_transcript(transcript: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits transcript into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.create_documents([transcript])

    return chunks

# ---------- Embedding Model ----------

_embeddings = None
def create_embeddings():
    """
    Creates HuggingFace embedding model.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings


# ---------- Vector Store ----------
def create_vector_store(transcript: str):
    """
    Creates FAISS vector store from transcript.
    """
    chunks = split_transcript(transcript)

    embeddings = create_embeddings()

    vector_store = FAISS.from_documents(chunks,embeddings)

    return vector_store


# ---------- Retriever ----------
def create_retriever(vector_store, k: int = 4):
    """
    Creates retriever from vector store.
    """

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})

    return retriever


# ---------- Complete Pipeline ----------
def create_video_retriever(transcript: str):
    """
    Transcript
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    FAISS
        ↓
    Retriever
    """

    vector_store = create_vector_store(transcript)

    retriever = create_retriever(vector_store)

    return retriever