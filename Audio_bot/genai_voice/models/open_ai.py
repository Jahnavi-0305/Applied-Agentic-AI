"""LLM - llm.py"""
from typing import Optional
from openai import OpenAI

from genai_voice.config.defaults import Config
from genai_voice.logger.log_utils import LogLevels, log
from genai_voice.models.model_config import ModelGenerationConfig
from genai_voice.defintions.model_response_formats import ModelResponseFormat


class CustomOpenAIModel:
    """LLM"""

    def __init__(
        self,
        api_key: str,
        model_name_and_version: str = Config.MODEL_GPT_TURBO_NAME,
        response_format: ModelResponseFormat = ModelResponseFormat.TEXT,
        model_seed: int = 0,
        log_level: LogLevels = LogLevels.ON,
    ) -> None:
        self.log_level = log_level
        self.model_name_and_version = model_name_and_version
        self.model_config = ModelGenerationConfig()
        self.model_config.generation["temperature"] = Config.TEMPERATURE
        self.model_config.generation["top_p"] = Config.TOP_P
        self.model_config.generation["top_k"] = Config.TOP_K
        self.model_config.generation["max_output_tokens"] = Config.MAX_OUTPUT_TOKENS
        self.model_config.generation["seed"] = model_seed
        self.model_config.generation["response_format"] = {
            "type": (
                "text" if response_format == ModelResponseFormat.TEXT else "json_object"
            )
        }
        log("Creating the OpenAI Model Client.")
        self.client = OpenAI(api_key=api_key)
        log(f"Initialized OpenAI model: {self.model_name_and_version}", log_level)

    @property
    def config(self) -> ModelGenerationConfig:
        """Config property"""
        return self.model_config

    @property
    def model_name(self) -> str:
        """Model name property"""
        return self.model_name_and_version

    def build_prompt(self, prompt: str, context: str) -> dict:
        """Build prompt for LLM"""
        prompt_template = {}
        if self.model_name.startswith("gpt"):
            prompt_template = {
                "role": "system",
                "content": f""" \
                            "{prompt}"
                            "{context}"
                            """,
            }
        else:
            log("This module supports only OpenAI GPT Models. Returning empty template.")
        return prompt_template

    def generate(self, messages: list, config: Optional[ModelGenerationConfig]):
        """Send the message to the model to get a response"""
        if not messages:
            raise ValueError("Messages are empty.")
        if not config:
            config = self.model_config
        if self.log_level == LogLevels.ON:
            log(config)
        gen_cfg = config.generation
        response = self.client.chat.completions.create(
            model=self.model_name_and_version,
            messages=messages,
            temperature=gen_cfg["temperature"],
            seed=gen_cfg["seed"],
            top_p=gen_cfg["top_p"],
            max_tokens=gen_cfg["max_output_tokens"],
            response_format=gen_cfg["response_format"],
        )
        if len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            raise ValueError(f"OpenAI didn't return any content: {response}")


if __name__ == "__main__":
    test_model = CustomOpenAIModel(api_key=Config.OPENAI_API_KEY)
    test_config = test_model.config
    test_prompt = test_model.build_prompt(prompt="What is the capital of the world?", context="")
    test_messages = [test_prompt]
    print(test_config)
    print(type(test_config))
    answer = test_model.generate(messages=test_messages, config=test_config)
    log(answer)
