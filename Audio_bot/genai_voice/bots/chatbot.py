"""Customizable Chatbot Main Functions"""

import os
import threading
from typing import Optional, Any

from dotenv import load_dotenv
from genai_voice.processing.audio import Audio
from genai_voice.models.open_ai import CustomOpenAIModel
from genai_voice.config.defaults import Config
from genai_voice.logger.log_utils import log, LogLevels

from genai_voice.defintions.prompts import (
    TRAVEL_AGENT_PROMPT,
    PROMPTS_TO_CONTEXT_DATA_FILE,
)

# load environment variables from .env file
load_dotenv(override=True)


class ChatBot:
    """ChatBot Class"""

    def __init__(
        self,
        prompt: Optional[str] = None,
        context_file_path: Optional[str] = None,
        model_name: str = Config.MODEL_GPT_TURBO_NAME,
        mic_id: Any = None,
        enable_speakers: bool = False,
        threaded: bool = False,
    ) -> None:
        """
        Initialize the chatbot
        mic_id:          The index of the mic to enable
        enable_speakers: Whether or not audio will be played
        threaded:        Plays back audio in seperate thread, can interfere with speech detector
        """
        if not prompt:
            prompt = TRAVEL_AGENT_PROMPT
            context_file_path = PROMPTS_TO_CONTEXT_DATA_FILE[TRAVEL_AGENT_PROMPT]

        log(f"Context file: {context_file_path}", log_level=LogLevels.ON)

        # Ensure our context file exists
        self.context_file_path = os.path.join("data", context_file_path)
        if not os.path.exists(self.context_file_path):
            raise ValueError(
                f"Provided context file path does not exist: {self.context_file_path}"
            )
        self.model_name = model_name
        match self.model_name:
            case Config.MODEL_GPT_TURBO_NAME:
                self.__client = CustomOpenAIModel(api_key=Config.OPENAI_API_KEY)
            case _:
                raise ValueError(f"Model {self.model_name} is not currently supported.")

        # Whether or not to use speakers
        self.__enable_speakers = enable_speakers

        # Whether or not to thread playback
        self.__threaded = threaded

        # Initialize audio library
        self.audio = Audio()

        # Initialize mic
        if mic_id is not None:
            self.initialize_microphone(mic_id)

        # Get data for LLM Context
        self.context = self.get_context_data()

        # Get initial prompt
        self.prompt = prompt

        # Prompt template to initialize LLM
        self.llm_prompt = self.__client.build_prompt(
            prompt=self.prompt, context=self.context
        )

    def get_completion_from_messages(self, messages):
        """
        Send the message to the specified OpenAI model
        """
        # use default config for model
        return self.__client.generate(messages=messages, config=None)

    def get_context_data(self) -> str:
        """Get the data for the LLM"""
        with open(self.context_file_path, "r", encoding="utf-8") as f:
            data = "".join(line for line in f)
        return data

    def respond(self, prompt, llm_history: list = None):
        """
        Get a response based on the current history
        """
        if not llm_history:
            log("Empty history. Creating a state list to track histories.")
            llm_history = []
        context = [self.llm_prompt]
        for interaction in llm_history:
            context.append({"role": "user", "content": f"{interaction[0]}"})
            context.append({"role": "assistant", "content": f"{interaction[1]}"})

        context.append({"role": "user", "content": f"{prompt}"})
        llm_response = self.get_completion_from_messages(context)

        if self.__enable_speakers:
            # With threads
            if self.__threaded:
                speaker_thread = threading.Thread(
                    target=self.audio.communicate, args=(llm_response,)
                )
                speaker_thread.start()
            # Without threads
            else:
                self.audio.communicate(llm_response)
        return llm_response

    def initialize_microphone(self, mic_id):
        """
        Initialize microphone object with the indicated ID.
        For best results a headset with a mic is recommended.
        """
        self.audio.initialize_microphone(mic_id)

    def recognize_speech_from_mic(self):
        """
        Listens for speech
        return: The text of the captured speech
        """
        return self.audio.recognize_speech_from_mic()

    def communicate(self, message):
        """
        Plays a message on the speakers
        message: the message
        """
        self.audio.communicate(message)

    def get_prompt_from_streamlit_audio(self, audio) -> str:
        """Converts audio captured from streamit to text"""
        if not audio:
            return None
        return self.audio.transcribe_from_transformer(audio)

    def get_prompt_from_gradio_audio(self, audio):
        """
        Converts audio captured from gradio to text.
        See https://www.gradio.app/guides/real-time-speech-recognition for more info.
        audio: object containing sampling frequency and raw audio data
        """
        log(f"Getting prompt from audio device: {audio}")
        if not audio:
            return None
        return self.audio.get_prompt_from_gradio_audio(audio)

    def get_prompt_from_file(self, file):
        """
        Converts audio from a file to text.
        file: the path to the audio file
        """

        return self.audio.get_prompt_from_file(file)


if __name__ == "__main__":
    # Enable speakers (adjust to True or False as needed)
    ENABLE_SPEAKERS = True

    # pylint: disable=invalid-name
    human_prompt = ""
    history = []

    # Create the chatbot
    chatbot = ChatBot(enable_speakers=ENABLE_SPEAKERS)

    # Main loop
    while human_prompt != "goodbye":
        response = chatbot.respond(human_prompt, history)
        history.append([human_prompt, response])
        human_prompt = input(f"\n{response}\n\n")
