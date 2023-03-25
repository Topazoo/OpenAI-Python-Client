import openai
from ...base import OpenAI_Client
from ...mixins import Chat_Context_Manager_Mixin
from ...enums import ROLE, CHAT_MODELS

# Example concrete client using the base client and a mixin
class Chat_Bot_Client(OpenAI_Client, Chat_Context_Manager_Mixin):
    _model = CHAT_MODELS.GPT_3_5_TURBO
    _api = openai.ChatCompletion
    _supported_models = CHAT_MODELS

    def run_prompt(self, temperature: float = 0):
        """ Sends a prompt to OpenAI """

        # Call the API and get a response
        result = self._api.create(model=self._model, messages=self.get_context(), temperature=temperature or self._temperature)

        try:
            # If valid, save it in context to be passed on future requests
            response = result["choices"][0]["message"]["content"]
            if response:
                self.add_statement(ROLE.ASSISTANT, response)
                return response
            
        except Exception:
            raise Exception("Failed to get a response from OpenAI API")
        

    def get_user_input(self):
        """ Get user input to send to the chatbot, save for future requests """

        # Get a question from the user and store is
        user_input = input('>>> ')
        
        self.add_statement(ROLE.USER, user_input)
