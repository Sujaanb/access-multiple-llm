import os
import sys
from dotenv import load_dotenv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage

import util.constants as constants
from util.cache_and_cost import CacheManager

class LLMFactory:

    @staticmethod
    def get_model_name():
        """
        Returns the model name based on the environment variable.
        """
        load_dotenv(override=True)
        env_name = os.getenv("llm_provider", "")

        model_mapping = {
            "mistral": constants.mistral_llm,
            "gemini": constants.gemini_llm,
            "openai": constants.openai_llm,
        }
        try:
            return model_mapping[env_name]
        except KeyError:
            raise ValueError(
                "Invalid environment name. Must be 'mistral', 'gemini', 'openai'."
            )

    @staticmethod
    def get_api_key():
        """
        Returns the API key based on the model/environment.
        """
        load_dotenv(override=True)
        env_name = os.getenv("llm_provider", "")

        api_key_mapping = {
            "mistral": os.getenv("mistral_api_key"),
            "gemini": os.getenv("gemini_api_key"),
            "openai": os.getenv("openai_api_key"),
        }

        try:
            return api_key_mapping[env_name]
        except KeyError:
            raise ValueError(
                "Invalid environment name. Must be 'mistral', 'gemini', or 'openai'."
            )

    @staticmethod
    def create_llm_instance(temperature=0.3, local_llm=False):
        """
        Creates and returns an instance of the appropriate LLM.
        """
        if local_llm:
            # If local_llm is True, use the local LLM instance.
            return ChatOllama(
                model=constants.local_llm,  # Use exact model name from 'ollama list'
                base_url=os.getenv("local_model_url"),  # Ollama server URL
            )
        model_name = LLMFactory.get_model_name()
        api_key = LLMFactory.get_api_key()

        if model_name == constants.mistral_llm:
            return ChatMistralAI(
                api_key=api_key, model_name=model_name, temperature=temperature
            )
        elif model_name == constants.openai_llm:
            return ChatOpenAI(
                api_key=api_key, model=model_name, temperature=temperature
            )
        elif model_name == constants.gemini_llm:
            return ChatGoogleGenerativeAI(
                api_key=api_key, model=model_name, temperature=temperature
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    @staticmethod
    def invoke(
        system_prompt: str = None,
        human_message: str = None,
        temperature=0.3,
        local_llm=False,
        use_cache=True
    ):
        """
        Invokes the LLM with given prompts using ChatPromptTemplate.
        
        Args:
            system_prompt: System message for the LLM
            human_message: User query/message
            temperature: Temperature for response generation
            local_llm: Whether to use local LLM via Ollama
            use_cache: Whether to use caching and cost tracking (default: True)
            
        Returns:
            LLM response or AIMessage object
        """
        cache_manager = CacheManager()
        
        # Check cache first if enabled
        if use_cache and system_prompt and human_message:
            cached_response = cache_manager.get_cached_response(system_prompt, human_message)
            if cached_response:
                # Return as AIMessage to maintain consistency
                return AIMessage(content=cached_response)
        
        # Create LLM instance
        llm = LLMFactory.create_llm_instance(temperature, local_llm)

        # Prepare and invoke
        if system_prompt and human_message:
            system_prompt = system_prompt.replace("{", "{{").replace("}", "}}")
            human_message = human_message.replace("{", "{{").replace("}", "}}")
            prompt_obj = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(system_prompt),
                    HumanMessagePromptTemplate.from_template(human_message),
                ]
            )
            formatted_messages = prompt_obj.format_messages()
            response = llm.invoke(formatted_messages)

        elif human_message:
            human_message = human_message.replace("{", "{{").replace("}", "}}")
            response = llm.invoke(human_message)

        else:
            raise ValueError("At least a human_message must be provided.")

        # Cache and track costs if enabled
        if use_cache:
            # Estimate tokens (rough approximation)
            tokens_used = len((system_prompt or "") + human_message) // 4
            
            # Save to cache
            cache_manager.save_response(system_prompt, human_message, response.content, tokens_used)
            
            # Track cost if not using local LLM
            if not local_llm:
                load_dotenv(override=True)
                provider = os.getenv("llm_provider", "mistral")
                cost = cache_manager.track_cost(provider, tokens_used)
                print(f"💰 Estimated cost: ${cost:.6f}")
        
        return response
