import os, openai, time, logging

# Typing
from ..enums import MODELS, COMPLETION_MODELS

class OpenAI_Client():
    ''' Base client to interact with the OpenAI API '''

    # Base API Key
    _api_key = ""
    # Base Temperature
    _temperature = 0
    # Base Model
    _model = COMPLETION_MODELS.TEXT_DAVINCI_002
    # Base API Endoint
    _api = openai.Completion
    # Base number of API call retries
    _max_retries = 3
    # Base ms between retries
    _ms_between_retries = 500
    # Base models supported
    _supported_models = MODELS

    def __init__(self, api_key:str=None, defaul_model_name:str="", default_temperature:float=0, max_retries:int=3, ms_between_retries:int=500) -> None:

        # Read passed API key but default to reading from environmental variables
        openai.api_key = self._api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self._api_key:
            raise ValueError("OpenAI API key must be set")

        # Read passed default model but default to reading from environmental variables
        self._model = self._validate_model(defaul_model_name or os.environ.get('OPENAI_DEFAULT_MODEL', self._model))

        # Read passed default temperature but default to reading from environmental variables
        self._temperature = default_temperature or os.environ.get('OPENAI_DEFAULT_TEMPERATURE', self._temperature)

        # Read passed default maximum call retries default to reading from environmental variables
        self._max_retries = max_retries or os.environ.get('OPENAI_MAX_RETRIES', self._max_retries)

        # Read passed default milliseconds to wait before call retries
        self._ms_between_retries = ms_between_retries or os.environ.get('OPENAI_MS_BETWEEN_RETRIES', self._ms_between_retries)

        # Replace self._api.create() with the interceptor function so we have a hook to
        # manage the result of calls from mixins (e.g. to filter results)
        self._create = self._api.create
        self._api.create = self._api_call_interceptor
    

    def _validate_model(self, model_name:str) -> str:
        ''' Validates if a passed model is valid for the client '''

        if model_name not in self._supported_models:
            logging.warn(f"\n\nThe model [{model_name}] is not supported for this client [{self.__class__}]. If this is not a custom fine-tuned model this is likely an error!\n")
            
        return model_name
    

    def _api_call_interceptor(self, **kwargs):
        # TODO - Mixin for metadata tracking
        """ Internal interceptor for calls made to the model. Useful for tracking response
            data per-call independent of what a user actually does with it.

            In the base class this just handles errors. Mixins can extend this to track 
            metadata, filter results, etc.
        """

        num_retries = 0
        # Ensure one call fires even for 0 retries
        while num_retries <= self._max_retries:
            try:
                return self._create(**kwargs)

            except Exception as e:
                new_error = self._handle_api_error(e)
                # If a new error should be thrown
                if new_error:
                    raise new_error

                # Backoff
                time.sleep((num_retries + 1) ** 2 * (self._ms_between_retries * .001))
                num_retries += 1


    def _handle_api_error(self, e:Exception):
        """ Handle API errors - Can be overridden """

        error_type = type(e)

        # Handle API error here, e.g. retry and log
        if error_type in [openai.error.APIError, openai.error.ServiceUnavailableError]:
            logging.warn(f"[Retrying] {e}")

        # Handle connection error here
        elif error_type == openai.error.APIConnectionError:
            return IOError(f"Failed to connect to OpenAI API: {e}")

        # Handle rate limit error (we recommend using exponential backoff)
        elif error_type == openai.error.RateLimitError:
            logging.warn(f"OpenAI API request exceeded rate limit: {e}")

        # Re-throw unknown errors
        else:
            return e


    def run_prompt(self, prompt:str, model:str=None, temperature:float=None):
        # Allow the model and temperature to be specified per call, but fall back on defaults
        model = model or self._model
        temperature = temperature or self._temperature

        return self._api.create(prompt=prompt, model=model, temperature=temperature)
