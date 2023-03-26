# typing
from typing import List, Union
from ..enums import ROLE

class Example:
    """
    A class that contains two strings, one representing an example input a
    completion model could receive and the other the response the model should generate.

    This data can be formatted to be fed to the model with the proper spacing using the str() call.

    An example of Example:
    ```
    Example('Tweet: "I loved the new Batman movie!"', 'Sentiment: "Positive"')
    ```
    """

    def __init__(self, example_input:str, example_output:str):
        self.example_input = example_input
        self.example_output = example_output

    def __str__(self) -> str:
        return f"\n{self.example_input}\n{self.example_output}\n"


class Example_Context_Manager_Mixin:
    """ Manages OpenAI Completion Context
    
    More specifically, this acts as a cache of two things:
    1. An overall directive (e.g. "Decide whether a Tweet's sentiment is positive, neutral, or negative.")
    2. A list of "examples" of some inputs and acceptable outputs for the model
    """

    # Permanent "job" of the completion AI, like "Decide whether a Tweet's sentiment is positive, neutral, or negative."
    _directive:str

    # Examples that will be passed to the AI of expected inputs and outputs with proper formatting
    _examples:List[Example] = []

    def __init__(self, directive:str, examples:List[Example]=None):
        self._directive = directive
        self._examples = examples or []

    def add_examples(self, examples:Union[Example, List[Example]]):
        """ Add an example or list of examples to the list of stored examples """

        if isinstance(examples, Example):
            self._examples.append(examples)
        elif isinstance(examples, list):
            self._examples += examples
        else:
            raise TypeError(f"add_examples() must be passed an Example or list of Example objects not [{type(examples)}]")
    
    def get_directive(self) -> str:
        """ Get core directive """

        return self._directive
    
    def get_examples(self, idx:int=None) -> Union[Example, List[Example]]:
        """ Get all examples or an example by index """

        return self._examples if not idx else self._examples[idx]

    def get_context(self) -> str:
        """ Get a combination of the core directive and examples to feed to the AI """

        if self._directive:
            examples = ''.join([str(example) for example in self._examples])
            context = f"{self._directive}\n{examples}"
            
            return context
        
        return ""
    
    def get_context_in_chatbot_format(self, prompt:str=None):
        """ Bridge for codegen modules that now use the chat models """

        context = []
        if self._directive:
            context.append({"role": ROLE.SYSTEM, "content": self._directive})
        
        if self._examples:
            context.append({"role": ROLE.USER, "content": "Examples:\n"})

            for example in self._examples:
                context.append({"role": ROLE.USER, "content": str(example)})

        if prompt:
            context.append({"role": ROLE.USER, "content": prompt})

        return context
