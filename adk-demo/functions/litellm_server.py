from litellm import CustomLLM
import litellm


class DummyLLM(CustomLLM):
    
    def completion(self, *args, **kwargs) -> litellm.ModelResponse:
        """
        Simple completion that adds "hello" prefix to the last message
        """
        print(f"Zhao {kwargs['model']}")
        # Get the last message content
        last_message = kwargs['messages'][-1]["content"]
        
        # Create response with "hello" prefix
        response = {
            "id": "dummy-response-id",
            "object": "chat.completion",
            "created": 1234567890,
            "model": kwargs['model'],
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"hello {last_message}"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(kwargs['messages']),
                "completion_tokens": len(last_message) + 6,  # 6 for "hello "
                "total_tokens": len(kwargs['messages']) + len(last_message) + 6
            }
        }
        return response

    def acompletion(self, *args, **kwargs) -> litellm.ModelResponse:
        """
        Async version - since we're using FastAPI, make this a regular method
        that's called from an async endpoint
        """
        
        return self.completion(*args, **kwargs)
