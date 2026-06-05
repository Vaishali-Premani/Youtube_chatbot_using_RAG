import streamlit as st
from rag.transcript import get_transcript_from_url
from rag.llm import answer_query
from rag.vector_store import create_video_retriever


# ---------- Page Configuration ----------
st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="wide"
)

# ---------- Session State Initialization ----------
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False


st.title("🎥 YouTube Chatbot")
# st.caption("Ask questions about any YouTube video using RAG")
if st.session_state.video_processed:
    st.info("Ask questions about the processed video.")
else:
    st.info("Paste a YouTube URL and process the video first.")


# ---------- Sidebar ----------
with st.sidebar:

    st.header("🎥 Video Processing")

    youtube_url = st.text_input(
        "Paste YouTube Video URL"
    )

    col1, col2 = st.columns(2)

    with col1:
        process_button = st.button(
            "Process",
            use_container_width=True
        )

    with col2:
        clear_button = st.button(
            "Reset",
            use_container_width=True
        )

    if clear_button:
        st.session_state.retriever = None
        st.session_state.messages = []
        st.session_state.video_processed = False
        st.rerun()

    if process_button:

        if not youtube_url.strip():
            st.error("Please enter a YouTube URL.")

        else:
            try:
                with st.spinner("Fetching transcript and building knowledge base..."):

                    transcript = get_transcript_from_url(
                        youtube_url
                    )

                    retriever = create_video_retriever(
                        transcript
                    )

                    st.session_state.retriever = retriever
                    st.session_state.video_processed = True

                    # Clear previous chat when loading new video
                    st.session_state.messages = []

                st.success("Video processed successfully!")

            except Exception as e:
                st.error(str(e))

    st.divider()

    if st.session_state.video_processed:
        st.success("✅ Video Ready")
    else:
        st.warning("⚠️ No Video Loaded")


# ---------- Display Chat History ----------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input(
    "Ask a question about the video...",
    disabled=not st.session_state.video_processed
)

# ---------- Handle User Query ----------
if user_query:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Check if video is processed
    if st.session_state.retriever is None:

        warning_message = (
            "Please process a YouTube video first."
        )

        with st.chat_message("assistant"):
            st.warning(warning_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": warning_message
            }
        )

    else:

        try:

            with st.chat_message("assistant"):

                with st.spinner("Generating answer..."):

                    answer = answer_query(
                        query=user_query,
                        retriever=st.session_state.retriever
                    )
                    answer = answer.strip()

                    st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_message = f"Error: {str(e)}"

            with st.chat_message("assistant"):
                st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )