import os, openai

class OpenAPI_Client():
    ''' Base client to interact with the OpenAI API '''

    _api_key = ""
    _temperature = 0
    _model = "text-davinci-003"
    _api = openai.Completion

    def __init__(self, api_key:str=None, defaul_model_name:str="", default_temperature=0) -> None:

        # Read passed API key but default to reading from environmental variables
        openai.api_key = self._api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self._api_key:
            raise ValueError("OpenAI API key must be set")

        # TODO - Models enum check
        # Read passed default model but default to reading from environmental variables
        self._model = defaul_model_name or os.environ.get('OPENAI_DEFAULT_MODEL', self._model)

        # Read passed default temperature but default to reading from environmental variables
        self._temperature = default_temperature or os.environ.get('OPENAI_DEFAULT_TEMPERATURE', self._temperature)


    def run_prompt(self, prompt:str, model:str=None, temperature:float=None):
        # Allow the model and temperature to be specified per call, but fall back on defaults
        model = model or self._model
        temperature = temperature or self._temperature

        return self._api.create(prompt=prompt, model=model, temperature=temperature)
