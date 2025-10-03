"""Script to run the gradio as code"""

import gradio as gr
from genai_voice.bots.chatbot import ChatBot
from genai_voice.logger.log_utils import log, LogLevels


# poetry run RunChatBotScript
def run():
    """Run Chatbot app"""
    chatbot = ChatBot(enable_speakers=True, threaded=True)
    history = []

    def get_response(audio):
        """Get Audio Response From Chatbot"""
        if not audio:
            raise ValueError("No audio file provided.")
        prompt = chatbot.get_prompt_from_gradio_audio(audio)
        log(f"Transcribed prompt: {prompt}", log_level=LogLevels.ON)
        response = chatbot.respond(prompt, history)
        history.append([prompt, response])
        return response

    demo = gr.Interface(
        get_response,
        gr.Audio(sources="microphone"),
        "text",
        title="Wanderwise Travel Assistant",
    )
    demo.launch()


# poetry run RunChatBotScript
def run_with_file_support():
    """Run Chatbot app and save files to disk"""
    chatbot = ChatBot(enable_speakers=True, threaded=True)
    history = []

    def get_response_from_file(file):
        prompt = chatbot.get_prompt_from_file(file)
        response = chatbot.respond(prompt, history)
        history.append([prompt, response])
        return response

    # Approach that doesn't have the warning but uses temp files
    demo = gr.Interface(
        get_response_from_file,
        gr.Audio(sources="microphone", type="filepath"),
        "text",
    )
    demo.launch()
