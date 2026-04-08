# Access Multiple LLMs

A unified Python framework for seamlessly accessing and switching between multiple Large Language Model (LLM) providers. This project provides a consistent, easy-to-use interface for working with **Mistral**, **Gemini**, **OpenAI**, and **local models** (via Ollama).

---

## 🎯 Overview

This project eliminates the complexity of managing multiple LLM provider APIs by providing:
- **Unified Interface**: Single entry point for all LLM providers
- **Easy Provider Switching**: Change providers by updating a single environment variable
- **Factory Pattern Implementation**: Clean, extensible architecture
- **LangChain Integration**: Leverages LangChain for robust LLM interaction
- **Flexible Temperature Control**: Fine-tune response creativity per invocation

---

## ✨ Key Features Implemented

### 1. **Multi-Provider Support**
   - ✅ **Mistral AI** - `mistral-large-latest`
   - ✅ **Google Gemini** - `gemini-1.5-flash`
   - ✅ **OpenAI** - `gpt-4.1-nano-2025-04-14`
   - ✅ **Local Models** - Via Ollama (`llama3.2:3b` by default)

### 2. **LLMFactory Class**
   A robust factory implementation providing:
   - `get_model_name()` - Retrieves model name from environment configuration
   - `get_api_key()` - Fetches appropriate API key based on selected provider
   - `create_llm_instance()` - Creates and returns LLM instance with configurable temperature
   - `invoke()` - Flexible method to send prompts to LLMs with optional system prompts

### 3. **Environment-Based Configuration**
   - Simple `.env` file configuration for provider selection
   - Support for multiple API keys (auto-selected based on provider)
   - Local model URL configuration for Ollama
   - No hardcoded credentials

### 4. **LangChain Prompt Templates**
   - Structured `SystemMessagePromptTemplate` and `HumanMessagePromptTemplate`
   - `ChatPromptTemplate` for managing conversation flow
   - Special character escaping for safe prompt formatting

### 5. **System Prompts Module**
   - Pre-built system prompts for common tasks
   - Currently includes `prompt_generate_summary` for text summarization
   - Easily extensible for additional use cases

### 6. **Built-in Use Cases**
   - **Text Summarization**: Generate concise summaries of input text
   - Extensible architecture for custom use cases

### 7. **Flexible Temperature Configuration**
   - Per-invocation temperature control (0.0 - 1.0)
   - Default temperature: 0.3 (deterministic responses)
   - Adjustable for different use cases (0.7 for creative tasks, etc.)

### 8. **Local LLM Support**
   - Seamless integration with Ollama for running models locally
   - `local_llm` parameter in `invoke()` method
   - No API key required for local models

---

## 📋 Prerequisites

Make sure you have the following installed:

- Python **3.8+**
- Git
- pip (Python package manager)
- A code editor like **VSCode**, **Cursor**, or **WindSurf**
- (Optional) **Ollama** - For running local LLMs

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

- **Mistral**: [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys)
- **Google Gemini**: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **OpenAI**: [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

> **Note:** Not all API keys are required. Provide keys only for the providers you plan to use.

### 5. Create a `.env` File

Create a `.env` file in the root directory:

```ini
# Select your preferred LLM provider
llm_provider = "mistral"  # Options: "mistral", "gemini", "openai"

# API Keys (leave empty if not used)
mistral_api_key = "your_mistral_api_key_here"
gemini_api_key = "your_gemini_api_key_here"
openai_api_key = "your_openai_api_key_here"

# Local Model Configuration (for Ollama)
local_model_url = "http://localhost:11434"
```

> **Important:** 
> - Only the API key for your selected `llm_provider` needs to be populated
> - Leave other keys empty if you don't plan to use those providers
> - For local models, ensure Ollama is running on the specified URL

---

## 📦 Dependencies

All dependencies are managed through `requirements.txt`:

```
langchain-mistralai          # LangChain + Mistral integration
langchain-openai             # LangChain + OpenAI integration
langchain-ollama             # LangChain + Ollama integration
langchain-google-genai       # LangChain + Google Gemini integration
langchain-core               # Core LangChain library
langchain-community          # Community LangChain components
python-dotenv                # Environment variable management
```

---

## ▶️ Usage Examples

### Basic Text Summarization

```bash
python test_run.py
```

This will generate a summary of the default query using your selected LLM provider.

### Using the LLMFactory in Your Code

```python
from util.llm_factory import LLMFactory

# Example 1: Simple query
response = LLMFactory.invoke(
    human_message="What is machine learning?",
    temperature=0.5
)
print(response.content)

# Example 2: With system prompt
response = LLMFactory.invoke(
    system_prompt="You are a helpful assistant.",
    human_message="Explain quantum computing in simple terms.",
    temperature=0.7
)
print(response.content)

# Example 3: Using local model
response = LLMFactory.invoke(
    human_message="Tell me a joke",
    temperature=0.8,
    local_llm=True
)
print(response.content)
```

### Switching Between Providers

Simply update the `llm_provider` value in your `.env` file and the application will automatically use the new provider:

```ini
# Before
llm_provider = "mistral"

# After
llm_provider = "gemini"
```

No code changes required!

---

## 🏗️ Project Structure

```
access-multiple-llm/
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── test_run.py                # Example usage script
└── util/
    ├── __init__.py            # Package initializer
    ├── constants.py           # LLM model definitions
    ├── llm_factory.py         # Main factory implementation
    └── system_prompt.py       # Pre-built system prompts
```

---

## 📚 Architecture

### Factory Pattern Implementation

The `LLMFactory` class implements the Factory design pattern for clean, extensible code:

```
User Code
    ↓
LLMFactory.invoke()
    ↓
LLMFactory.create_llm_instance()
    ↓
├─ LLMFactory.get_model_name() → Model Selection
├─ LLMFactory.get_api_key() → Credential Management
    ↓
├─ ChatMistralAI (Mistral)
├─ ChatOpenAI (OpenAI)
├─ ChatGoogleGenerativeAI (Gemini)
└─ ChatOllama (Local Models)
```

---

## 🔧 Extending Support

### Adding a New LLM Provider

1. **Update `util/constants.py`:**
```python
anthropic_llm = "claude-3-opus"
```

2. **Update `util/llm_factory.py`:**
```python
def get_model_name(self):
    model_mapping = {
        # ... existing providers
        "anthropic": constants.anthropic_llm,
    }

def create_llm_instance(self, temperature=0.3, local_llm=False):
    # ... existing code
    elif model_name == constants.anthropic_llm:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=api_key, model=model_name, temperature=temperature
        )
```

3. **Update `.env` file:**
```ini
anthropic_api_key = "your_api_key"
```

4. **Install required package:**
```bash
pip install langchain-anthropic
```

---

## 🐛 Error Handling

The application includes robust error handling:

- **Invalid Provider**: Raises `ValueError` if an unsupported provider is specified
- **Missing API Key**: Raises an error if the required API key is not configured
- **Connection Issues**: LangChain handles connection failures gracefully
- **Invalid Prompts**: Escaping special characters prevents template errors

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add support for new LLM providers
- Create additional system prompts
- Improve documentation
- Report issues or suggest features

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙋 Support & Questions

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Review the setup instructions above
3. Ensure your API keys are correctly configured
4. Verify that required dependencies are installed

---

## 🎓 Educational Purpose

This project serves as an excellent learning resource for:
- Factory design pattern implementation
- LLM API integration
- LangChain framework usage
- Environment-based configuration management
- Python best practices

Happy coding! 🚀