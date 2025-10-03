"""Moderation.py"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from genai_voice.defintions.prompts import BAD_PROMPT, GOOD_PROMPT

# load environment variables from .env file
load_dotenv(override=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
response = client.moderations.create(input=[BAD_PROMPT, GOOD_PROMPT])

for result in response.results:
    if result.flagged:
        print("something bad")
    else:
        print("something good")
    # print(result.categories)
