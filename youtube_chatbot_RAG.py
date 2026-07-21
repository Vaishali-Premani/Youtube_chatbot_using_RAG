# ---------- Importing Libraries and Environment Variables ----------
import re 
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()


# ---------- Input Youtube Video Link and extract the Video ID ----------
link = input('Enter video link: ')
match = re.search(r"v=([^&]+)", link)
if match:
    video_id = (match.group(1))
    
    
# ---------- Fetch Transcript from the video ----------
try:
    fetched_transcript = YouTubeTranscriptApi().fetch(video_id=video_id, languages=['en'])
    transcript = ''
    # for snippet in fetched_transcript:
    #     transcript = transcript + snippet.text
    transcript = ' '.join(snippet.text for snippet in fetched_transcript)
    # print(transcript)
except TranscriptsDisabled:
    print("No captions available for this video.")


# ---------- Text Splitting/Chunking ----------
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
)
chunks = splitter.create_documents([transcript])
# print(len(chunks))


# ---------- Chunk Embedding and Store in Vector space ----------
embeddings = HuggingFaceEmbeddings(
    model='sentence-transformers/all-MiniLM-L6-v2'
)

vector_store = FAISS.from_documents(chunks, embeddings)
# print(vector_store.index_to_docstore_id)
# results = vector_store.similarity_search("What is neural network?", k=2 )
# print(results)


# ---------- Retriever ----------
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':4})
# print(retriever)


# ---------- LLM creation ----------
llm = HuggingFaceEndpoint(
    repo_id = "meta-llama/Llama-3.1-8B-Instruct",
    task='text generation', 
    temperature= 0.2
)
model = ChatHuggingFace(llm=llm)


# ---------- Prompt ----------
prompt = PromptTemplate(
    template = """
    You are a helpful assistant. Answer the question based on the transcript context given to you only.
    If you don't know the answer, just reply that you don't know rather than generating the answer from your own.
    
    {context}
    
    question : {query}
    """    ,    
    input_variables= ['context', 'query']
)

# ---------- User input ----------
while True:
    user_query = input("Enter your query (write 'exit' to end the conversation): ")
    
    if user_query.strip().lower() == 'exit':
        print("EXITING ...")
        break
    
    retrieved_docs = retriever.invoke(user_query)
    
    context_text = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    
    final_prompt = prompt.invoke({'context':context_text, 'query':user_query})
    
    answer = model.invoke(final_prompt)
    
    print(answer.content)
    
    