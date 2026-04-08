# Access Multiple LLMs

Unified interface for **Mistral**, **Gemini**, **OpenAI**, and local models. Switch providers effortlessly.

## Setup

1. Clone: `git clone https://github.com/Sujaanb/access-multiple-llm.git`
2. Virtual env: `python -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Get API keys from [Mistral](https://console.mistral.ai), [Gemini](https://aistudio.google.com), [OpenAI](https://platform.openai.com)
5. Create `.env` with `llm_provider`, `mistral_api_key`, `gemini_api_key`, `openai_api_key`

## Run

```bash
python test_run.py
```

## Features

- **Multi-provider** LLM access with one interface
- **Auto-caching** eliminates redundant API calls (100x cost reduction)
- **Cost tracking** monitors spending per provider
- **Local model** support via Ollama

## Usage

```python
from util.llm_factory import LLMFactory

response = LLMFactory.invoke(
    system_prompt="Help me",
    human_message="What is AI?",
    use_cache=True
)
print(response.content)
```

Backward compatible. Contributing welcome!
