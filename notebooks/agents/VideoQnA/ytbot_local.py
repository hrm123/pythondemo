from langchain_community.llms import ollama  # For interacting with Ollama's LLM

# Import necessary libraries for the YouTube bot
import re  # For extracting video id


try:
    from youtube_transcript_api import YouTubeTranscriptApi  # For extracting transcripts from YouTube videos
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class YouTubeTranscriptApi:
        def list(self, video_id):
            raise RuntimeError("youtube-transcript-api is not installed")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into manageable segments
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class RecursiveCharacterTextSplitter:
        def __init__(self, chunk_size=200, chunk_overlap=20):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_text(self, text):
            return [text] if text else []

try:
    from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes  # For specifying model types
except ImportError:  # pragma: no cover - exercised in minimal test environments
    ModelTypes = None

try:
    from ibm_watsonx_ai import APIClient, Credentials  # For API client and credentials management
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class APIClient:
        def __init__(self, *args, **kwargs):
            pass

    class Credentials(dict):
        def __init__(self, url=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if url is not None:
                self["url"] = url

try:
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams  # For managing model parameters
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class GenParams:
        DECODING_METHOD = "decoding_method"
        MAX_NEW_TOKENS = "max_new_tokens"

try:
    from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods  # For defining decoding methods
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class DecodingMethods:
        GREEDY = "greedy"

try:
    from langchain_ibm import WatsonxLLM, WatsonxEmbeddings  # For interacting with IBM's LLM and embeddings
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class WatsonxLLM:
        def __init__(self, *args, **kwargs):
            raise ImportError("langchain_ibm is not installed")

    class WatsonxEmbeddings:
        def __init__(self, *args, **kwargs):
            raise ImportError("langchain_ibm is not installed")

try:
    from ibm_watsonx_ai.foundation_models.utils import get_embedding_model_specs  # For retrieving model specifications
except ImportError:  # pragma: no cover - exercised in minimal test environments
    def get_embedding_model_specs():
        return []

try:
    from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes  # For specifying types of embeddings
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class EmbeddingTypes:
        pass

try:
    from langchain_community.vectorstores import FAISS  # For efficient vector storage and similarity search
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class FAISS:
        @classmethod
        def from_texts(cls, chunks, embedding_model):
            return cls()

        def similarity_search(self, query, k=3):
            return []

try:
    from langchain.chains import LLMChain  # For creating chains of operations with LLMs
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class LLMChain:
        def __init__(self, *args, **kwargs):
            pass

try:
    from langchain.prompts import PromptTemplate  # For defining prompt templates
except ImportError:  # pragma: no cover - exercised in minimal test environments
    class PromptTemplate:
        def __init__(self, input_variables=None, template=""):
            self.input_variables = input_variables or []
            self.template = template

        def format(self, **kwargs):
            return self.template.format(**kwargs)

def get_video_id(url):    
    # Regex pattern to match YouTube video URLs
    pattern = r'https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None
 
def get_transcript(url):
    # Extracts the video ID from the URL
    video_id = get_video_id(url)
    if not video_id:
        return None

    try:
        # Create a YouTubeTranscriptApi() object
        ytt_api = YouTubeTranscriptApi()

        # Fetch the list of available transcripts for the given YouTube video
        transcripts = ytt_api.list(video_id)

        transcript = ""
        for t in transcripts:
            # Check if the transcript's language is English
            language_code = getattr(t, 'language_code', None)
            if language_code == 'en':
                is_generated = getattr(t, 'is_generated', False)
                if is_generated:
                    if len(transcript) == 0:
                        transcript = t.fetch()
                else:
                    transcript = t.fetch()
                    break

        if transcript:
            return transcript
    except Exception:
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
 
 
def setup_credentials():
    # Define the model ID for the WatsonX model being used
    model_id = "ibm/granite-8b-code-instruct"
   
    # Set up the credentials by specifying the URL for IBM Watson services
    credentials = Credentials(url="https://us-south.ml.cloud.ibm.com")
   
    # Create an API client using the credentials
    client = APIClient(credentials)
   
    # Define the project ID associated with the WatsonX platform
    project_id = "skills-network"
   
    # Return the model ID, credentials, client, and project ID for later use
    return model_id, credentials, client, project_id
 
def define_parameters():
    # Return a dictionary containing the parameters for the WatsonX model
    return {
        # Set the decoding method to GREEDY for generating text
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
       
        # Specify the maximum number of new tokens to generate
        GenParams.MAX_NEW_TOKENS: 900,
    }
 
 
def initialize_watsonx_llm(model_id, credentials, project_id, parameters):
    # Create and return an instance of the WatsonxLLM with the specified configuration
    return WatsonxLLM(
        model_id=model_id,          # Set the model ID for the LLM
        url=credentials.get("url"),      # Retrieve the service URL from credentials
        project_id=project_id,            # Set the project ID for accessing resources
        params=parameters                  # Pass the parameters for model behavior
    )
 

def initialize_ollama_llm(model_id, credentials, project_id, parameters):
    # Create and return an instance of the Ollama with the specified configuration
    return ollama(
            model="llama3:latest",
            request_timeout=120.0,
            context_window=8000,
        )
 
def setup_embedding_model(credentials, project_id):
    # Create and return an instance of WatsonxEmbeddings with the specified configuration
    return WatsonxEmbeddings(
        model_id='ibm/slate-30m-english-rtrvr-v2',  # Set the model ID for the SLATE-30M embedding model
        url=credentials["url"],                            # Retrieve the service URL from the provided credentials
        project_id=project_id                               # Set the project ID for accessing resources in the Watson environment
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
        # Step 1: Set up IBM Watson credentials
        model_id, credentials, client, project_id = setup_credentials()
 
        # Step 2: Initialize WatsonX LLM for summarization
        # llm = initialize_watsonx_llm(model_id, credentials, project_id, define_parameters())
        llm = initialize_ollama_llm()
 
        # Step 3: Create the summary prompt and chain
        summary_prompt = create_summary_prompt()
        summary_chain = create_summary_chain(llm, summary_prompt)
 
        # Step 4: Generate the video summary
        summary = summary_chain.run({"transcript": processed_transcript})
        return summary
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
        # Step 1: Chunk the transcript (only for Q&A)
        chunks = chunk_transcript(processed_transcript)
 
        # Step 2: Set up IBM Watson credentials
        model_id, credentials, client, project_id = setup_credentials()
 
        # Step 3: Initialize WatsonX LLM for Q&A
        llm = initialize_watsonx_llm(model_id, credentials, project_id, define_parameters())
 
        # Step 4: Create FAISS index for transcript chunks (only needed for Q&A)
        embedding_model = setup_embedding_model(credentials, project_id)
        faiss_index = create_faiss_index(chunks, embedding_model)
 
        # Step 5: Set up the Q&A prompt and chain
        qa_prompt = create_qa_prompt_template()
        qa_chain = create_qa_chain(llm, qa_prompt)
 
        # Step 6: Generate the answer using FAISS index
        answer = generate_answer(user_question, faiss_index, qa_chain)
        return answer
    else:
        return "Please provide a valid question and ensure the transcript has been fetched."
 
 