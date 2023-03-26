import openai
from ...base import OpenAI_Client
from ...mixins import Example_Context_Manager_Mixin, Example

# Typing
from typing import List
from ...enums import COMPLETION_MODELS, CHAT_MODELS

class Completion_Client(OpenAI_Client, Example_Context_Manager_Mixin):
    """ Text completion client that allows user specified examples to be passed to the model """

    _model = COMPLETION_MODELS.TEXT_DAVINCI_003
    _api = openai.Completion
    _supported_models = COMPLETION_MODELS

    def __init__(self, directive:str, examples:List[Example]=None, api_key:str=None, defaul_model_name:str="", default_temperature:float=0, max_retries:int=3, ms_between_retries:int=500) -> None:
        super().__init__(api_key, defaul_model_name, default_temperature, max_retries, ms_between_retries)
        Example_Context_Manager_Mixin.__init__(self, directive=directive, examples=examples)


    def run_prompt(self, prompt:str, temperature: float = 0) -> str:
        """ Sends a prompt to OpenAI with the context stored by the mixin """

        # Call the API and get a response
        result = self._api.create(model=self._model, prompt=self.get_context() + prompt, temperature=temperature or self._temperature)

        try:
            # If valid, save it in context to be passed on future requests
            response = result["choices"][0]["text"]
            if response:
                return response
            
        except Exception:
            raise Exception("Failed to get a response from OpenAI API")


class Code_Completion_Client(Completion_Client):
    """ Code completion client that allows user specified examples to be passed to the model 
        Currently this uses chat models rather than specific codex models
    """
    
    _model = CHAT_MODELS.GPT_3_5_TURBO
    _api = openai.ChatCompletion
    _supported_models = CHAT_MODELS

    def __init__(self, directive:str="", examples:List[Example]=None, api_key:str=None, defaul_model_name:str="", default_temperature:float=0, max_retries:int=3, ms_between_retries:int=500) -> None:
        super().__init__(directive, examples, api_key, defaul_model_name, default_temperature, max_retries, ms_between_retries)


    def run_prompt(self, prompt:str, temperature: float = 0) -> str:
        """ Sends a prompt to OpenAI with the context stored by the mixin """

        # Call the API and get a response
        result = self._api.create(model=self._model, messages=self.get_context_in_chatbot_format(prompt), temperature=temperature or self._temperature)

        try:
            # If valid, save it in context to be passed on future requests
            response = result["choices"][0]["message"]["content"]
            if response:
                return response
            
        except Exception:
            raise Exception("Failed to get a response from OpenAI API")