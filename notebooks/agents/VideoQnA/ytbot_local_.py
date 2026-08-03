# Import necessary libraries for the YouTube bot
import re  #For extracting video id
from youtube_transcript_api import YouTubeTranscriptApi  # For extracting transcripts from YouTube videos
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into manageable segments
from langchain_community.llms import Ollama  # For interacting with Ollama's LLM
from langchain_community.embeddings import OllamaEmbeddings  # For interacting with Ollama's embeddings
from langchain_community.vectorstores import FAISS  # For efficient vector storage and similarity search
from langchain.chains import LLMChain  # For creating chains of operations with LLMs
from langchain.prompts import PromptTemplate  # For defining prompt templates
# import http.cookiejar
# import browser_cookie3


def get_video_id(url):    
    # Regex pattern to match YouTube video URLs
    pattern = r'https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None
'''
def export_youtube_cookies(output_file="youtube_cookies.txt"):
    # 1. Automatically fetch all cookies from Chrome (or use .firefox(), .edge(), etc.)
    try:
        cj = browser_cookie3.chrome(domain_name=".youtube.com")
    except Exception as e:
        print(f"Error accessing browser database: {e}")
        print("Please ensure your browser is completely closed before running.")
        return

    # 2. Initialize a Netscape-compatible cookie jar
    netscape_jar = http.cookiejar.MozillaCookieJar(output_file)

    # 3. Filter and transfer YouTube cookies into the Netscape jar
    for cookie in cj:
        if "youtube.com" in cookie.domain:
            netscape_jar.set_cookie(cookie)

    # 4. Save the cookies to the file
    netscape_jar.save(ignore_discard=True, ignore_expires=True)
    print(f"Successfully exported YouTube cookies to {output_file}!")
 '''

def get_transcript(url):
    # Extracts the video ID from the URL
    video_id = get_video_id(url)
    if not video_id:
        return None

    try:
        # Create a YouTubeTranscriptApi() object
        ytt_api = YouTubeTranscriptApi()
       # example url - https://www.youtube.com/watch?v=LNHBMFCzznE
        # Fetch the list of available transcripts for the given YouTube video
        # export_youtube_cookies()  # Export cookies to a file for authentication
        transcripts = ytt_api.list(video_id)
       
        transcript = ""
        for t in transcripts:
            # Check if the transcript's language is English
            language_code = getattr(t, 'language_code', None)
            if language_code == 'en':
                is_generated = getattr(t, 'is_generated', False)
                if is_generated:
                    # If no transcript has been set yet, use the auto-generated one
                    if len(transcript) == 0:
                        transcript = t.fetch() # is not working because youtube says IP blocked
                else:
                    # If a manually created transcript is found, use it (overrides auto-generated)
                    transcript = t.fetch()
                    break  # Prioritize the manually created transcript, exit the loop
       
        if transcript:
            return transcript
    except Exception as e:
        print(e)
        pass

    return [{"text": "Transcript unavailable in this environment.", "start": 0.0, "duration": 0.0}]


def process(transcript):
    # Initialize an empty string to hold the formatted transcript
    if transcript is None:
        return ""

    if isinstance(transcript, str):
        return transcript.rstrip() + "\n" if transcript else ""

    if isinstance(transcript, dict):
        transcript = [transcript]

    txt = ""

    if isinstance(transcript, (list, tuple)):
        for item in transcript:
            if isinstance(item, dict):
                text = item.get("text")
                start = item.get("start")
            else:
                text = getattr(item, "text", None)
                start = getattr(item, "start", None)

            if text is None:
                continue

            if start is None:
                txt += f"Text: {text}\n"
            else:
                txt += f"Text: {text} Start: {start}\n"

    return txt


def chunk_transcript(processed_transcript, chunk_size=2, chunk_overlap=0):
    text = process(processed_transcript)
    if not text:
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    chunks = []
    start = 0
    while start < len(lines):
        end = min(start + chunk_size, len(lines))
        chunk_lines = lines[start:end]
        if chunk_lines:
            chunks.append("\n".join(chunk_lines))
        if end >= len(lines):
            break
        start += chunk_size - chunk_overlap

    return chunks
 

 
def initialize_watsonx_llm(model_id, credentials, project_id, parameters):
    # Retained for compatibility/stubbing if needed
    return initialize_ollama_llm()

def initialize_ollama_llm(model_id="llama3", base_url="http://localhost:11434"):
    # Create and return an instance of the Ollama with the specified configuration
    return Ollama(
        model=model_id,
        base_url=base_url,
        temperature=0.0
    )
 
def setup_embedding_model(credentials=None, project_id=None):
    # Setup Ollama embeddings using all-minilm:latest
    return OllamaEmbeddings(
        model="all-minilm:latest",
        base_url="http://localhost:11434"
    )
 
 
 
def create_faiss_index(chunks, embedding_model):
    """
    Create a FAISS index from text chunks using the specified embedding model.
   
    :param chunks: List of text chunks
    :param embedding_model: The embedding model to use
    :return: FAISS index
    """
    # Use the FAISS library to create an index from the provided text chunks
    return FAISS.from_texts(chunks, embedding_model)
 
 
 
def perform_similarity_search(faiss_index, query, k=3):
    """
    Search for specific queries within the embedded transcript using the FAISS index.
   
    :param faiss_index: The FAISS index containing embedded text chunks
    :param query: The text input for the similarity search
    :param k: The number of similar results to return (default is 3)
    :return: List of similar results
    """
    # Perform the similarity search using the FAISS index
    results = faiss_index.similarity_search(query, k=k)
    return results
 
 
def create_summary_prompt():
    """
    Create a PromptTemplate for summarizing a YouTube video transcript.
   
    :return: PromptTemplate object
    """
    # Define the template for the summary prompt
    template = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an AI assistant tasked with summarizing YouTube video transcripts. Provide concise, informative summaries that capture the main points of the video content.
 
    Instructions:
    1. Summarize the transcript in a single concise paragraph.
    2. Ignore any timestamps in your summary.
    3. Focus on the spoken content (Text) of the video.
 
    Note: In the transcript, "Text" refers to the spoken words in the video, and "start" indicates the timestamp when that part begins in the video.<|eot_id|><|start_header_id|>user<|end_header_id|>
    Please summarize the following YouTube video transcript:
 
    {transcript}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
   
    # Create the PromptTemplate object with the defined template
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template=template
    )
   
    return prompt
 
 
def create_summary_chain(llm, prompt, verbose=True):
    """
    Create an LLMChain for generating summaries.
   
    :param llm: Language model instance
    :param prompt: PromptTemplate instance
    :param verbose: Boolean to enable verbose output (default: True)
    :return: LLMChain instance
    """
    return LLMChain(llm=llm, prompt=prompt, verbose=verbose)
 
 
def retrieve(query, faiss_index, k=7):
    """
    Retrieve relevant context from the FAISS index based on the user's query.
 
    Parameters:
        query (str): The user's query string.
        faiss_index (FAISS): The FAISS index containing the embedded documents.
        k (int, optional): The number of most relevant documents to retrieve (default is 3).
 
    Returns:
        list: A list of the k most relevant documents (or document chunks).
    """
    relevant_context = faiss_index.similarity_search(query, k=k)
    return relevant_context
 
def create_qa_prompt_template():
    """
    Create a PromptTemplate for question answering based on video content.
    Returns:
        PromptTemplate: A PromptTemplate object configured for Q&A tasks.
    """
   
    # Define the template string
    qa_template = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an expert assistant providing detailed and accurate answers based on the following video content. Your responses should be:
    1. Precise and free from repetition
    2. Consistent with the information provided in the video
    3. Well-organized and easy to understand
    4. Focused on addressing the user's question directly
    If you encounter conflicting information in the video content, use your best judgment to provide the most likely correct answer based on context.
    Note: In the transcript, "Text" refers to the spoken words in the video, and "start" indicates the timestamp when that part begins in the video.<|eot_id|>
 
    <|start_header_id|>user<|end_header_id|>
    Relevant Video Context: {context}
    Based on the above context, please answer the following question:
    {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    # Create the PromptTemplate object
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=qa_template
    )
    return prompt_template
 
 
def create_qa_chain(llm, prompt_template, verbose=True):
    """
    Create an LLMChain for question answering.
 
    Args:
        llm: Language model instance
            The language model to use in the chain (e.g., WatsonxGranite).
        prompt_template: PromptTemplate
            The prompt template to use for structuring inputs to the language model.
        verbose: bool, optional (default=True)
            Whether to enable verbose output for the chain.
 
    Returns:
        LLMChain: An instantiated LLMChain ready for question answering.
    """
   
    return LLMChain(llm=llm, prompt=prompt_template, verbose=verbose)
 
 
def generate_answer(question, faiss_index, qa_chain, k=7):
    """
    Retrieve relevant context and generate an answer based on user input.
 
    Args:
        question: str
            The user's question.
        faiss_index: FAISS
            The FAISS index containing the embedded documents.
        qa_chain: LLMChain
            The question-answering chain (LLMChain) to use for generating answers.
        k: int, optional (default=3)
            The number of relevant documents to retrieve.
 
    Returns:
        str: The generated answer to the user's question.
    """
 
    # Retrieve relevant context
    relevant_context = retrieve(question, faiss_index, k=k)
 
    # Generate answer using the QA chain
    answer = qa_chain.predict(context=relevant_context, question=question)
 
    return answer
 
 
# Initialize an empty string to store the processed transcript after fetching and preprocessing
processed_transcript = ""
 
def summarize_video(video_url):
    """
    Title: Summarize Video
 
    Description:
    This function generates a summary of the video using the preprocessed transcript.
    If the transcript hasn't been fetched yet, it fetches it first.
 
    Args:
        video_url (str): The URL of the YouTube video from which the transcript is to be fetched.
 
    Returns:
        str: The generated summary of the video or a message indicating that no transcript is available.
    """
    global fetched_transcript, processed_transcript
   
   
    if video_url:
        # Fetch and preprocess transcript
        fetched_transcript = get_transcript(video_url)
        processed_transcript = process(fetched_transcript)
    else:
        return "Please provide a valid YouTube URL."
 
    if processed_transcript:
        try:
            # Step 1: Set up IBM Watson credentials (kept for compatibility/tests)
            # model_id, credentials, client, project_id = setup_credentials()
 
            # Step 2: Initialize Ollama LLM for summarization
            llm = initialize_ollama_llm()
 
            # Step 3: Create the summary prompt and chain
            summary_prompt = create_summary_prompt()
            summary_chain = create_summary_chain(llm, summary_prompt)
 
            # Step 4: Generate the video summary
            return summary_chain.run({"transcript": processed_transcript})
        except Exception as exc:
            return f"Unable to summarize this video right now. Ollama initialization failed: {exc}"
    else:
        return "No transcript available. Please fetch the transcript first."
 
 
def answer_question(video_url, user_question):
    """
    Title: Answer User's Question
 
    Description:
    This function retrieves relevant context from the FAISS index based on the user’s query
    and generates an answer using the preprocessed transcript.
    If the transcript hasn't been fetched yet, it fetches it first.
 
    Args:
        video_url (str): The URL of the YouTube video from which the transcript is to be fetched.
        user_question (str): The question posed by the user regarding the video.
 
    Returns:
        str: The answer to the user's question or a message indicating that the transcript
             has not been fetched.
    """
    global fetched_transcript, processed_transcript
 
    # Check if the transcript needs to be fetched
    if not processed_transcript:
        if video_url:
            # Fetch and preprocess transcript
            fetched_transcript = get_transcript(video_url)
            processed_transcript = process(fetched_transcript)
        else:
            return "Please provide a valid YouTube URL."
 
    if processed_transcript and user_question:
        try:
            # Step 1: Chunk the transcript (only for Q&A)
            chunks = chunk_transcript(processed_transcript)
 
 
            # Step 3: Initialize Ollama LLM for Q&A
            llm = initialize_ollama_llm()
 
            # Step 4: Create FAISS index for transcript chunks (only needed for Q&A)
            embedding_model = setup_embedding_model()
            faiss_index = create_faiss_index(chunks, embedding_model)
 
            # Step 5: Set up the Q&A prompt and chain
            qa_prompt = create_qa_prompt_template()
            qa_chain = create_qa_chain(llm, qa_prompt)
 
            # Step 6: Generate the answer using FAISS index
            return generate_answer(user_question, faiss_index, qa_chain)
        except Exception as exc:
            return f"Unable to answer this question right now. Ollama initialization failed: {exc}"
    else:
        return "Please provide a valid question and ensure the transcript has been fetched."
 
 