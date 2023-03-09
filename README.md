# OpenAI API Python Client

A (very rough WIP) Python Client for OpenAI APIs.

## Overview

Right now this just provides a base client that allows a reusable way to do common things
(like loading the API key) plus some easy overrides (like which model to use) and some mixins 
for when state dependence is important

## Example

All I've got in lieu of real docs for now :). Run a local chatbot from your command line:

1. Export your OpenAI token

```sh
export OPENAI_API_KEY=AKIAIOSFODNN7EXAMPLE
```

1. Clone the repo (I'll throw up a PyPi package before too long)

1. Use the base class and mixins to create apps!

```python
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
        user_input = input('>>> ')
        
        self.add_statement(ROLE.USER, user_input)


# Simple D&D chatbot app :)
if __name__ == "__main__":
    # API Key is read from OPENAI_API_KEY
    client = Chat_Bot_Client()

    # Add a high level directive
    client.add_directive("You are a Dungeons and Dragons Dungeon Master. Use the 5th edition of the Dungeons and Dragons Player Handbook, Dungeon Master Guide, and Monster Manual")
    client.add_directive("At the beginning of your chat with the user you will assist them in creating a character. This character will have a description and stats as outlined in the 5th edition of the Dungeons and Dragons Player Handbook.")
    client.add_directive("Let the user choose race and class before assigning a personality, stats, and starting inventory. Provide the user with a list of races and classes they can be. Tell the user they can ask for more details about a class or race")
    client.add_directive("Once you introduce the character, give the player the start of an adventure campaign and ask the player what they would like to do")
    client.add_directive("As outlined in the handbook, if a roll is necessary based on the situation, roll for the user")
    client.add_directive("Finish by asking the player what they'd like to do next")


    # Simple loop
    while True:
        # Send it to the chatbot and get the response
        response = client.run_prompt()
        # Print the response
        print("\n" + response + "\n")
        # Get question from the user
        client.get_user_input()
```

## Contributing

Contributions are welcome! Please not the following when contributing:

- Unittests must be added under the `tests/` directory for the PR to be approved. You can run unittests from the root project directory with the following command:

    ```sh
    python setup.py test
    ```

- PRs cannot be merged without all unittests passing (they will execute automatically)
- Merges to `main` will automatically create a new release on PyPi **[unless it is from a forked Repo](https://stackoverflow.com/questions/58737785/github-actions-empty-env-secrets)**
