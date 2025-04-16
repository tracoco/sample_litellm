from litellm import CustomLLM, ModelResponse
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import time

def anthropic_to_litellm_response(anthropic_message: Any, model_name: str, prompt: str) -> ModelResponse:
    """
    Convert an Anthropic message to litellm.ModelResponse format.
    
    Args:
        anthropic_message: The response from Anthropic API
        model_name: The name of the Anthropic model used
        prompt: The original prompt sent to the model
        
    Returns:
        A litellm.ModelResponse object representing the Anthropic response
    """
    # Extract the content from Anthropic's message
    content = anthropic_message['content'][0]['text'] if anthropic_message['content'] else ""
    
    # Create message dict with default content
    message = {
        "content": content,
        "role": "assistant"
    }
    
    # Check for function calls in the content items
    if anthropic_message['content']:
        for item in anthropic_message['content']:
            if item['type'] and item['type'] == 'tool_use':
                # Initialize tool_calls if not present
                if 'tool_calls' not in message:
                    message['tool_calls'] = []
                
                # Extract function call information
                tool_call = {
                    "id": item['id'] if item['id'] else f"call_{len(message['tool_calls'])}",
                    "type": "function",
                    "function": {
                        "name": item['name'] if item['name']  else "",
                        "arguments": item['input']  if item['input']  else "{}"
                    }
                }
                message['tool_calls'].append(tool_call)
    
    # Create response object in the format expected by litellm
    response = ModelResponse(
        id=anthropic_message.id if hasattr(anthropic_message, 'id') else f"anthropic-{int(time.time())}",
        choices=[{
            "message": message,
            "index": 0,
            "finish_reason": "stop"
        }],
        created=int(time.time()),
        model=model_name,
        usage={
            "prompt_tokens": -1,  # Anthropic doesn't always provide token counts in the same format
            "completion_tokens": -1,
            "total_tokens": -1
        },
        _response_ms=None
    )
    
    # If anthropic_message has input_tokens and output_tokens, use them
    if hasattr(anthropic_message, 'usage') and anthropic_message.usage:
        if hasattr(anthropic_message.usage, 'input_tokens'):
            response.usage["prompt_tokens"] = anthropic_message.usage.input_tokens
        if hasattr(anthropic_message.usage, 'output_tokens'):
            response.usage["completion_tokens"] = anthropic_message.usage.output_tokens
        response.usage["total_tokens"] = (response.usage["prompt_tokens"] if response.usage["prompt_tokens"] >= 0 else 0) + \
                                       (response.usage["completion_tokens"] if response.usage["completion_tokens"] >= 0 else 0)
    
    return response