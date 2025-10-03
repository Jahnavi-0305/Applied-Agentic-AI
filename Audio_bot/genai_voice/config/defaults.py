"""Config"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv(override=True)


@dataclass
class Config:
    """LLM Config"""

    MODEL_GPT_TURBO_NAME = "gpt-4-turbo"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TEMPERATURE = 0.0
    TOP_P = 0.97
    TOP_K = 40
    MAX_OUTPUT_TOKENS = 2048
    WEB_SCRAPER_OUTPUT_FILE = "data/context.txt"

    def __repr__(self):
        return f"""
        Default(MODEL_GPT_TURBO_NAME='{self.MODEL_GPT_TURBO_NAME}', 
        OPENAI_API_KEY='{self.OPENAI_API_KEY}', 
        TEMPERATURE={self.TEMPERATURE}, 
        TOP_P={self.TOP_P}, 
        TOP_K={self.TOP_K}, 
        MAX_OUTPUT_TOKENS={self.MAX_OUTPUT_TOKENS}, 
        WEB_SCRAP_OUTPUT_DIR={self.WEB_SCRAPER_OUTPUT_FILE})"""


if __name__ == "__main__":
    default_config = Config()
    print(default_config)
