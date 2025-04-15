# ADK Custom LLM Examples

This project demonstrates two approaches to implementing custom LLMs using ADK (Agent Development Kit):

1. Direct LLM Implementation: Using a custom LLM directly with ADK
2. Server Implementation: Running a custom LLM as a FastAPI server

Both implementations demonstrate a simple "DummyLLM" that prefixes all responses with "hello".

## Project Structure

```
.
├── .gitignore
├── README.md
├── adk-demo/                # Direct LLM implementation
│   ├── config.yaml         # ADK configuration
│   └── functions/
│       ├── __init__.py
│       ├── agent.py        # ADK agent definition
│       └── litellm_server.py  # DummyLLM implementation
```

## Requirements

```bash
pip install "fastapi[all]" uvicorn litellm google-adk
```

## Approach 1: Direct LLM Implementation

This approach directly uses the custom LLM with ADK.

### Configuration (adk-demo/config.yaml)
```yaml
model:
  provider: litellm
  custom_llm: custom_llm.DummyLLM
  model: "dummy-model"
  temperature: 0.7
  max_tokens: 1000

functions:
  - path: functions
    name: agent
```

### Running Direct LLM Example

```bash
cd adk-demo
adk web 
```

Access the web interface at http://localhost:8000

## Approach 2: Server Implementation

This approach runs the custom LLM as a FastAPI server that follows the OpenAI API format.

### Running the Server

```bash
cd adk-demo/functions
python litellm_server.py
```

The server will start on http://localhost:8000

### Testing the Server

Using curl:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dummy-model",
    "messages": [
      {"role": "user", "content": "world"}
    ]
  }'
```

Expected response:
```json
{
  "id": "dummy-response-id",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "dummy-model",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "hello world"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 1,
    "completion_tokens": 11,
    "total_tokens": 12
  }
}
```

## Implementation Details

### DummyLLM Class

Both approaches use the same core DummyLLM class that:
1. Implements synchronous `completion` method
2. Implements asynchronous `acompletion` method
3. Prefixes all responses with "hello"

Key implementation:
```python
class DummyLLM(CustomLLM):
    async def acompletion(self: "DummyLLM",
                         model: str,
                         messages: List[Dict[str, str]],
                         **kwargs) -> Dict[str, Any]:
        # Explicitly use self to avoid binding issues
        return self.completion(model=model, messages=messages, **kwargs)
```

### Important Notes

1. The `acompletion` method must be implemented as an async method
2. Explicit self parameter typing helps prevent binding issues
3. Both approaches use the same response format for compatibility

## Development Tips

1. Use the ADK web interface for interactive testing
2. Monitor server logs for debugging
3. Test both sync and async methods
4. Ensure proper error handling

## Error Handling

Common errors and solutions:
- "missing self argument": Ensure proper method binding in async methods
- Connection errors: Verify server is running on correct port
- Invalid responses: Check response format matches OpenAI API

## Contributing

Feel free to contribute to this project by submitting pull requests or creating issues for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.