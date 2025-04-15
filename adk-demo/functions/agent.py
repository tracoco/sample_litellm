from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import litellm

from .litellm_server import DummyLLM

llm = DummyLLM()

litellm.custom_provider_map = [ # 👈 KEY STEP - REGISTER HANDLER
        {"provider": "dummylm", "custom_handler": llm}
    ]

root_agent = LlmAgent(
    model=LiteLlm(model="dummylm/Dummy"), # LiteLLM model string format
    name="dummy_agent",
    instruction="You are a helpful assistant powered by GPT-4o.",
    # ... other agent parameters
)

