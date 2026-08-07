

import torch
import os
import gradio as gr
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from transformers import pipeline  # For Speech-to-Text
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_community.llms import Ollama

'''
 Function to remove non-ASCII characters
'''
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)

'''
Function to create product assistant - The product_assistant function processes transcripts of the sample earnings call to ensure that financial product terms are correctly formatted. It uses a detailed system prompt to transform terms (e.g., '401k' to '401(k) retirement savings plan') and resolves contextual ambiguities for acronyms such as 'LTV'. Note that in this project, this assistant is specifically designed to work with financial terminology. However, you can customize its prompts to suit your unique use case.
It concatenates the user input with the prompt and sends it to a language model (meta-llama/llama-3-2-11b-vision-instruct) using the ModelInference class. Llama 3.2 collection represents a new generation of multimodal models that build upon the foundation established by Llama 3.1. Parameters such as temperature (randomness) and top_p (output diversity) customize the model's response. The function returns the formatted transcript after the model processes the input.
'''

def product_assistant(ascii_transcript):
    system_prompt = """You are an intelligent assistant specializing in financial products;
    your task is to process transcripts of earnings calls, ensuring that all references to
     financial products and common financial terms are in the correct format. For each
     financial product or common term that is typically abbreviated as an acronym, the full term 
    should be spelled out followed by the acronym in parentheses. For example, '401k' should be
     transformed to '401(k) retirement savings plan', 'HSA' should be transformed to 'Health Savings Account (HSA)' , 'ROA' should be transformed to 'Return on Assets (ROA)', 'VaR' should be transformed to 'Value at Risk (VaR)', and 'PB' should be transformed to 'Price to Book (PB) ratio'. Similarly, transform spoken numbers representing financial products into their numeric representations, followed by the full name of the product in parentheses. For instance, 'five two nine' to '529 (Education Savings Plan)' and 'four zero one k' to '401(k) (Retirement Savings Plan)'. However, be aware that some acronyms can have different meanings based on the context (e.g., 'LTV' can stand for 'Loan to Value' or 'Lifetime Value'). You will need to discern from the context which term is being referred to  and apply the appropriate transformation. In cases where numerical figures or metrics are spelled out but do not represent specific financial products (like 'twenty three percent'), these should be left as is. Your role is to analyze and adjust financial product terminology in the text. Once you've done that, produce the adjusted transcript and a list of the words you've changed"""

    # Concatenate the system prompt and the user transcript
    prompt_input = system_prompt + "\n" + ascii_transcript

    # Create a messages object
    messages = [
        HumanMessage(prompt_input)
    ]

    chat_model = ChatOllama(
        model="llama3",
        temperature=0.2,  # Controls randomness; lower values make the output more deterministic
        top_p=0.6              # Nucleus sampling to control output diversity
    )
    # bound_chat = chat_model.bind(temperature=0.2, top_p=0.9)
    # Send the input messages to the model and retrieve its response
    response = chat_model.invoke(messages)
    print("\n" + response.content)

    # Extract and return the content of the model's first response choice
    return response.content

#######------------- Prompt Template and Chain-------------#######

# Define the prompt template
template = """
Generate meeting minutes and a list of tasks based on the provided context.

Context:
{context}

Meeting Minutes:
- Key points discussed
- Decisions made

Task List:
- Actionable items with assignees and deadlines
"""

prompt = ChatPromptTemplate.from_template(template)


def initialize_ollama_llm(model_id="llama3", base_url="http://localhost:11434"):
    # Create and return an instance of the Ollama with the specified configuration
    return Ollama(
        model=model_id,
        base_url=base_url,
        temperature=0.0
    )

# Define the chain
chain = (
    {"context": RunnablePassthrough()}  # Pass the transcript as context
    | prompt
    | initialize_ollama_llm()
    | StrOutputParser()
)


#######------------- Speech2text and Pipeline-------------###

# Speech-to-text pipeline
def transcript_audio(audio_file):
    pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium.en",
    chunk_length_s=30,
    )

    raw_transcript = pipe(audio_file, batch_size=8)["text"]
    ascii_transcript = remove_non_ascii(raw_transcript)

    adjusted_transcript = product_assistant(ascii_transcript)
    result = chain.invoke({"context": adjusted_transcript})

    # Write the result to a file for downloading
    output_file = "meeting_minutes_and_tasks.txt"
    with open(output_file, "w") as file:
        file.write(result)

    # Return the textual result and the file for download
    return result, output_file

#######------------- Gradio Interface-------------#######

audio_input = gr.Audio(sources="upload", type="filepath", label="Upload your audio file")
output_text = gr.Textbox(label="Meeting Minutes and Tasks")
download_file = gr.File(label="Download the Generated Meeting Minutes and Tasks")

iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=[output_text, download_file],
    title="AI Meeting Assistant",
    description="Upload an audio file of a meeting. This tool will transcribe the audio, fix product-related terminology, and generate meeting minutes along with a list of tasks."
)

iface.launch(server_name="0.0.0.0", server_port=5000)
