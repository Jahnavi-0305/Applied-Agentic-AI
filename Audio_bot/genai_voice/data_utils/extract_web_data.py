"""Extract Web Data"""

import os

from typing import Optional
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_loaders import AsyncChromiumLoader

from genai_voice.config.defaults import Config
from genai_voice.logger.log_utils import log
from genai_voice.data_utils.urls import SAMPLE_URLS, HTML_TAGS_TO_TARGET

# Set the user agent for http requests identification
os.environ["USER_AGENT"] = "myagent"


def extract_webpage_data(out_file: Optional[str]):
    """Extract Web Page Data"""
    if not out_file:
        log(f"No output file, falling back to default: {Config.WEB_SCRAPER_OUTPUT_FILE}")
        out_file = Config.WEB_SCRAPER_OUTPUT_FILE
    if not os.path.exists(out_file):
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

    # Load HTML content using AsyncChromiumLoader
    log(f"Creating the AsyncChromiumLoader with #{len(SAMPLE_URLS)} urls...")
    try:
        loader = AsyncChromiumLoader(SAMPLE_URLS)
        docs = loader.load()
        log("Documents scraped.")

        # Transform the loaded HTML using BeautifulSoupTransformer
        log(f"Using BeautifulSoupTransformer to extract {HTML_TAGS_TO_TARGET}.")
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs, tags_to_extract=HTML_TAGS_TO_TARGET
        )
    except Exception as e:
        log("Failed to scrap data.")
        raise ValueError("Failed to scrap data successfully.") from e

    log(f"Transformed #{len(docs_transformed)} urls.")
    data = [doc.page_content for doc in docs_transformed]
    data = "".join(str(x + "\n\n") for x in data)
    log("Writing to output file.")
    with open(out_file, "w", encoding="utf-8") as file:
        file.write(data)
    log(f"Successfully written data to '{out_file}'")


# poetry run ExtractWebPagesAndSaveData
def run():
    """Run Web scraper"""
    log("Starting the web scraper...")
    extract_webpage_data(out_file=Config.WEB_SCRAPER_OUTPUT_FILE)
    log("Completed the web scraper...")
