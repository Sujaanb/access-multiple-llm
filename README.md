# Access Multiple LLMs

This project provides a unified interface to access multiple Large Language Models (LLMs) such as **Mistral**, **Gemini**, and **OpenAI**, with support for local models as well. It enables seamless switching between providers for experimentation, prototyping, or integration.

---

## 📋 Prerequisites

Make sure you have the following installed:

* Python **3.8+**
* Git
* A code editor like **VSCode**, **Cursor**, or **WindSurf**

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Sujaanb/access-multiple-llm.git
cd access-multiple-llm
```

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# For Windows (PowerShell):
./venv/Scripts/Activate

# For macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get API Keys

Obtain free API keys from the following providers:

* [Mistral](https://console.mistral.ai/api-keys)
* [Google Gemini](https://aistudio.google.com/app/apikey)
* (Optional) [OpenAI](https://platform.openai.com/account/api-keys)

### 5. Create a `.env` File

Create a `.env` file in the root directory with the following structure:

```ini
llm_provider = "mistral"  # Options: "mistral", "gemini", "openai"

mistral_api_key = ""      # Your Mistral API key (optional)

gemini_api_key = ""       # Your Gemini API key (optional)

openai_api_key = ""       # Your OpenAI API key (optional)

local_model_url = "http://localhost:11434"  # URL for local model (if used)
```

> **Note:** You can leave API keys empty if you don't have access to certain providers.
> The application will use the `llm_provider` you specify, as long as a valid API key is provided for it.
> Select the `llm_provider` as required among the three currently given options.

---

## ▶️ Run the Project

To execute a basic test using your selected provider:

```bash
python test_run.py
```

This will demonstrate the **caching and cost tracking** features by making the same query twice:
- **First call**: Hits the LLM API
- **Second call**: Uses the cached response (no API cost!)

---

## ✨ Features

### 🔄 Multiple LLM Provider Support

* [x] Mistral
* [x] Gemini
* [x] OpenAI
* [x] Local Model (via Ollama)

### 💾 Response Caching

- **Automatic caching** of LLM responses based on query hash
- **Eliminates redundant API calls** for identical queries
- **Faster responses** on cached queries (instant retrieval)
- **Reduces API costs** significantly over time

**How it works:**
1. When you make a query, it's converted to a hash
2. If that hash exists in cache, the stored response is returned instantly
3. Otherwise, the API is called and the response is cached for future use

### 💰 Cost Tracking

- **Automatic cost calculation** for each API call
- **Provider-specific pricing** based on token count
- **Cost summary** tracking across all providers
- **Helps monitor** API spending over time

**Cost tracking includes:**
- Total cost per provider
- Number of tokens used
- Number of API calls made
- Cumulative spending report

**Pricing (per 1M tokens):**
- Mistral: $0.15
- Gemini: $0.50
- OpenAI: $3.00

---

## 🧩 Usage Examples

### Basic Usage (with Caching Enabled)

```python
from util.llm_factory import LLMFactory
from util.system_prompt import prompt_generate_summary

# This will check cache first, then call API if needed
response = LLMFactory.invoke(
    system_prompt=prompt_generate_summary,
    human_message="What is climate change?",
    temperature=0.7,
    use_cache=True,  # Enable caching and cost tracking
)

print(response.content)
```

### Disable Caching (if needed)

```python
response = LLMFactory.invoke(
    system_prompt="You are a helpful assistant",
    human_message="Hello!",
    use_cache=False,  # Skip cache, always hit API
)
```

### View Cost Summary

```python
from util.cache_and_cost import CacheManager

cache_manager = CacheManager()
costs = cache_manager.get_cost_summary()
print(f"Total API Cost: ${costs['total_cost']}")
print(f"Breakdown: {costs['providers']}")
```

### Clear Cache

```python
from util.cache_and_cost import CacheManager

cache_manager = CacheManager()
cache_manager.clear_cache()  # Removes all cached responses
```

---

## 📁 Project Structure

```
access-multiple-llm/
├── util/
│   ├── __init__.py
│   ├── llm_factory.py          # Main LLM interface with caching
│   ├── cache_and_cost.py        # Cache management and cost tracking (NEW)
│   ├── constants.py             # LLM model names
│   └── system_prompt.py         # System prompts for different tasks
├── llm_cache/                   # Cache directory (auto-created, not in git)
│   ├── <hash>.json              # Cached responses
│   └── costs.json               # Cost tracking data
├── test_run.py                  # Demo script with caching demonstration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## 🧩 Extending Support

Support for additional LLM providers can be **easily extended** if required.

To add a new provider:

1. Add the provider to `util/constants.py`
2. Update `LLMFactory.get_model_name()` and `get_api_key()` methods
3. Add provider pricing to `CacheManager.PROVIDER_COSTS` in `util/cache_and_cost.py`
4. Implement the provider in `LLMFactory.create_llm_instance()`

Feel free to contribute or open an issue to request integration with other APIs.

---

## 📊 Cost Saving Example

Without caching (100 identical queries):
- Mistral: 100 API calls = $0.15 cost
- Time: Depends on network

With caching (100 identical queries):
- Mistral: 1 API call + 99 cache hits = $0.0015 cost
- Time: 1st query ~500ms, remaining ~10ms each
- **Savings: 100x cost reduction, 50x speed improvement** ⚡

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more LLM providers
- Improve caching strategies
- Add TTL (Time-to-Live) expiry for cached responses
- Implement persistent storage options
- Add rate limiting features

---

## 📝 License

This project is open source and available for educational and commercial use.

---
