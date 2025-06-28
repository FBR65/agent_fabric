# Agent Fabric

**Generate custom AI agents from natural language descriptions**

Agent Fabric is a powerful tool that allows you to create specialized AI agents simply by describing what you want them to do in plain language. The system analyzes your requirements and generates fully functional, standalone Python agents using PydanticAI with MCP and A2A compatibility.

## Features

- 🤖 **Natural Language Agent Creation** - Describe your agent in plain English/German
- 🎯 **Intelligent Specialization** - Automatically generates optimized system prompts for different use cases
- 📦 **Standalone Agents** - Each generated agent is a complete, runnable Python file
- 🔧 **MCP Integration** - Optional support for external tools and capabilities
- 🌐 **A2A Compatible** - Agents can be run as servers for integration with other applications
- 📱 **User-Friendly Interface** - Clean Gradio web interface with tabs and examples
- 📥 **Easy Download** - Direct download of generated agents and requirements

## Supported Agent Types

- **Code Conversion** - Convert code between programming languages
- **Text Processing** - Grammar correction, style optimization, proofreading
- **Sentiment Analysis** - Analyze emotions and sentiment in text
- **Translation** - Multi-language translation with cultural nuances
- **Summarization** - Extract key points and create summaries
- **Information Research** - Web search and information gathering
- **Programming** - Code generation and software development assistance

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Using uv (Recommended)

```bash
# Clone or download the project
cd agent_fabric

# Install dependencies
uv sync

# Start Agent Fabric
uv run python main.py
```

### Using pip

```bash
# Clone or download the project
cd agent_fabric

# Install dependencies
pip install -r requirements.txt

# Start Agent Fabric
python main.py
```

## Quick Start

1. **Start Agent Fabric**
   ```bash
   uv run python main.py
   ```

2. **Open your browser** to `http://localhost:7860`

3. **Describe your agent** in the text field:
   ```
   "Create an agent that corrects German grammar and improves text style"
   ```

4. **Configure settings** (optional):
   - Enable external tools for web search, time, etc.
   - Adjust LLM server settings if using custom endpoints

5. **Generate and download** your agent:
   - Click "Generate Agent"
   - Save and download the generated `.py` file and `requirements.txt`

## LLM Server Configuration

Agent Fabric supports various LLM providers:

### Ollama (Default)
```
Server: http://localhost:11434/v1
Model: qwen2.5:latest
API Key: sk-dummy
```

### LM Studio
```
Server: http://localhost:1234/v1
Model: your-model-name
API Key: sk-dummy
```

### OpenAI Compatible APIs
```
Server: https://api.openai.com/v1
Model: gpt-3.5-turbo
API Key: your-actual-api-key
```

## Using Generated Agents

Each generated agent is a standalone Python file with multiple usage modes:

### Interactive Mode
```bash
python your_agent.py
```

### Server Mode (A2A Compatible)
```bash
python your_agent.py server
```
Access at `http://localhost:8000`

### Installing Agent Dependencies
```bash
# In the same directory as your agent
pip install -r requirements.txt

# Or with uv
uv add pydantic-ai pydantic-ai-slim[a2a] fasta2a fastapi uvicorn
```

## Project Structure

```
agent_fabric/
├── main.py              # Gradio web interface
├── generator.py         # Agent code generator
├── requirements.txt     # Project dependencies
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Example Usage

### Creating a Code Converter Agent
```
Description: "I need a code converter from Python to Go"
Result: Specialized agent that converts Python code to idiomatic Go code
```

### Creating a Text Analysis Agent
```
Description: "Analyze sentiment in customer reviews and social media posts"
Result: Expert sentiment analysis agent with structured output
```

### Creating a Research Agent
```
Description: "Search for current news and information on any topic"
External Tools: ✓ Enabled
Result: Research agent with web search capabilities
```

## Advanced Features

### MCP Integration
Enable "External Tools" to give your agent access to:
- Web search via DuckDuckGo
- Current time and date
- Weather information
- PDF conversion
- Text anonymization

### A2A Compatibility
All generated agents are compatible with the Agent-to-Agent (A2A) protocol:
- Can be deployed as microservices
- Easy integration with other AI systems
- RESTful API endpoints
- Health check endpoints

## Troubleshooting

### Common Issues

**"Received empty model response"**
- Check if your LLM server is running
- Verify the model name is correct
- Test server connectivity

**Syntax errors in generated code**
- Usually caused by special characters in descriptions
- The system automatically escapes most issues

**Import errors when running agents**
- Install required dependencies: `pip install -r requirements.txt`
- Or use: `uv add pydantic-ai pydantic-ai-slim[a2a] fasta2a fastapi uvicorn`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Support

For issues and questions:
- Check the "Help" tab in the web interface
- Review this README
- Submit GitHub issues for bugs

---

**Agent Fabric** - Making AI agent creation accessible to everyone through natural language descriptions.
