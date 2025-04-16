from litellm import CustomLLM
import litellm
from .anthropic_adk import anthropic_to_litellm_response
from typing import List, Dict, Any
import time

class DummyLLM(CustomLLM):
    
    first_call = True

    def completion(self, *args, **kwargs) -> litellm.ModelResponse:
        """
        Simple completion that adds "hello" prefix to the last message
        """
        
        # Get the last message content
        last_message = kwargs['messages'][-1]["content"]
        
        # Create a mockup Anthropic message with a tool call
        anthropic_message = {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": f"dummy: {last_message}",
                }
            ]
        }

        if self.first_call:
            anthropic_message['content'].append({
                    "type": "tool_use",
                    "id": "toolu_01A09q90qw90lq917835lq9",
                    "name": "get_weather",
                    "input": {"city": last_message}
                })
            self.first_call = False
                        
        res = anthropic_to_litellm_response(anthropic_message, kwargs['model'], last_message)
        
        return res

    def acompletion(self, *args, **kwargs) -> litellm.ModelResponse:
        """
        Async version - since we're using FastAPI, make this a regular method
        that's called from an async endpoint
        """
        
        return self.completion(*args, **kwargs)
