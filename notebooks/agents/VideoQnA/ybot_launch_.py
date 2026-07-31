import os
import sys
from pathlib import Path


def ensure_gradio():
    try:
        import gradio as gr
        return gr
    except ModuleNotFoundError:
        venv_python = Path(__file__).resolve().parent / ".videoqna" / "Scripts" / "python.exe"
        if venv_python.exists():
            os.execv(str(venv_python), [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]])
        raise


gr = ensure_gradio()
from ytbot_local_ import summarize_video, answer_question


with gr.Blocks() as interface:
 
    gr.Markdown(
        "<h2 style='text-align: center;'>YouTube Video Summarizer and Q&A</h2>"
    )
 
    # Input field for YouTube URL
    video_url = gr.Textbox(label="YouTube Video URL", placeholder="Enter the YouTube Video URL")
   
    # Outputs for summary and answer
    summary_output = gr.Textbox(label="Video Summary", lines=5)
    question_input = gr.Textbox(label="Ask a Question About the Video", placeholder="Ask your question")
    answer_output = gr.Textbox(label="Answer to Your Question", lines=5)
 
    # Buttons for selecting functionalities after fetching transcript
    summarize_btn = gr.Button("Summarize Video")
    question_btn = gr.Button("Ask a Question")
 
    # Display status message for transcript fetch
    transcript_status = gr.Textbox(label="Transcript Status", interactive=False)
 
    # Set up button actions
    summarize_btn.click(summarize_video, inputs=video_url, outputs=summary_output)
    question_btn.click(answer_question, inputs=[video_url, question_input], outputs=answer_output)
 
# Launch the app with specified server name and port
interface.launch(server_name="0.0.0.0", server_port=7860, quiet=True, show_error=False)
