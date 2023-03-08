import os, openai

class OpenAPI_Client():
    ''' Client to interact with the OpenAI API '''

    _api_key = ""
    _temperature = 0
    _model = "text-davinci-003"

    def __init__(self, api_key:str=None, defaul_model_name:str="text-davinci-003", default_temperature=0) -> None:

        # Read passed API key but default to reading from environmental variables
        openai.api_key = self._api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self._api_key:
            raise ValueError("OpenAI API key must be set")

        # TODO - Models enum check
        # Read passed default model but default to reading from environmental variables
        self._model = defaul_model_name or os.environ.get('OPENAI_DEFAULT_MODEL')

        # Read passed default temperature but default to reading from environmental variables
        self._temperature = default_temperature or os.environ.get('OPENAI_DEFAULT_TEMPERATURE')


    def run_prompt(self, prompt:str, model:str=None, temperature:float=None):
        
        # Allow the model and temperature to be specified per call, but fall back on defaults
        model = model or self._model
        temperature = temperature or self._temperature

        return openai.Completion.create(prompt=prompt, model=model, temperature=temperature)
