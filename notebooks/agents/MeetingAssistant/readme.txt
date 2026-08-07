# create virtual environment using python3.10
python3.10 -m venv .meeting_assistant

# run following commands
.meeting_assistant\Scripts\activate
pip install -r requirements.text

# download the sound file by running following command
\.meeting_assistant\Scripts\python.exe downloader.py

# download ffmpeg for windows. Unzip it some folder and add that folder name to system environment path

meeting_assistant\Scripts\python.exe simple_speech2txt.py

# generates the text of speech in the downloaded file

# run the gradio demo website 
meeting_assistant\Scripts\python.exe hello.py

# run the gradio website that takes wav file as input and outputs the corresponding text of the speech in wav file
>.meeting_assistant\Scripts\python.exe speech2text_app.py

# upload any meeting audio from internet and see its text 
> \.meeting_assistant\Scripts\python.exe speech_analyzer.py