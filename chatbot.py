import openai
from .client import OpenAPI_Client
from .mixins import Chat_Context_Manager_Mixin
from .enums import ROLE

# Example concrete client using the base client and a mixin
class Chat_Bot_Client(OpenAPI_Client, Chat_Context_Manager_Mixin):
    _model = "gpt-3.5-turbo"
    _api = openai.ChatCompletion

    def run_prompt(self, temperature: float = 0):
        """ Sends a prompt to OpenAPI """

        # Call the API and get a response
        result = self._api.create(model=self._model, messages=self.get_context(), temperature=temperature or self._temperature)

        try:
            # If valid, save it in context to be passed on future requests
            response = result["choices"][0]["message"]["content"]
            if response:
                self.add_statement(ROLE.ASSISTANT, response)
                return response
            
        except Exception:
            raise Exception("Failed to get a response from OpenAPI")
        

    def get_user_input(self):
        """ Get user input to send to the chatbot, save for future requests """

        # Get a question from the user and store is
        user_input = input('What would you like to ask?\n>>> ')
        
        self.add_statement(ROLE.USER, user_input)


# Simple chatbot app :)
if __name__ == "__main__":
    # API Key is read from OPENAI_API_KEY
    client = Chat_Bot_Client()

    # Add a high level directive
    client.add_directive("You are a helpful chatbot who gives correct answers but adds in a joke")

    # Simple loop
    while True:
        # Get question from the user
        client.get_user_input()
        # Send it to the chatbot and get the response
        response = client.run_prompt()
        # Print the response
        print("\n" + response + "\n")
