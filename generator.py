from jinja2 import Template


class AgentGenerator:
    """Generator für PydanticAI Agenten basierend auf natürlicher Sprache."""

    def __init__(self):
        """Initialisiere den AgentGenerator mit einem Prompt-Engineering-Agent."""
        self.prompt_engineer = self._create_prompt_engineer()

    def _create_prompt_engineer(self):
        """Erstelle einen AI-Agent für intelligente System-Prompt-Generierung."""
        from pydantic_ai import Agent
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider
        import os

        # LLM Setup (aus Umgebung oder Standard)
        endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
        api_key = os.getenv("LLM_API_KEY", "sk-dummy")
        model_name = os.getenv("LLM_MODEL", "qwen2.5:latest")

        provider = OpenAIProvider(base_url=endpoint, api_key=api_key)
        model = OpenAIModel(provider=provider, model_name=model_name)

        system_prompt = """Du bist ein Experte für AI-Agent System-Prompt Engineering.

Analysiere die Nutzerbeschreibung und erstelle einen perfekt spezialisierten System-Prompt für den gewünschten AI-Agent.

WICHTIG: Verstehe was der Nutzer WIRKLICH will:
- Ein "Prompt Creator" soll verschiedene Prompt-Techniken anwenden
- Ein "Redenschreiber" soll Reden verfassen
- Ein "Code-Konverter" soll Code zwischen Sprachen konvertieren
- etc.

Der System-Prompt muss den Agent so konfigurieren, dass er GENAU das tut was beschrieben wurde.

Für Prompt Creator/Engineer: Erstelle einen System-Prompt der bei jeder Anfrage automatisch alle gängigen Prompt-Techniken (Zero-Shot, Few-Shot, Chain-of-Thought, Role-Based, Instruction-Following) anwendet.

Antworte NUR mit dem System-Prompt, keine Erklärungen."""

        return Agent(model=model, system_prompt=system_prompt, retries=2)

    def generate_agent(
        self,
        description: str,
        use_mcp: bool = False,
        llm_endpoint: str = "http://localhost:11434/v1",
        llm_api_key: str = "sk-dummy",
        llm_model: str = "qwen2.5:latest",
        filename: str = "generated_agent.py",
    ) -> str:
        """Generiere Agent-Code basierend auf Beschreibung."""

        template_content = self._get_base_template()
        template = Template(template_content)

        # Generiere System-Prompt basierend auf Beschreibung
        system_prompt = self._generate_system_prompt(description)

        # Generiere Pydantic-Response-Model basierend auf Beschreibung
        response_model = self._generate_response_model(description)

        code = template.render(
            description=description,
            system_prompt=system_prompt,
            response_model=response_model,
            use_mcp=use_mcp,
            llm_endpoint=llm_endpoint,
            llm_api_key=llm_api_key,
            llm_model=llm_model,
            filename=filename,
        )

        return code

    def _get_base_template(self) -> str:
        """Lade das Basis-Template für Agenten."""
        return '''#!/usr/bin/env python3
"""
Generierter Agent: {{ description }}
Erstellt mit Agent Fabric

Installationsanleitung:
1. pip install -r requirements.txt
2. python {{ filename }}

Oder mit uv:
1. uv add pydantic-ai pydantic-ai-slim[a2a] fasta2a fastapi uvicorn
2. python {{ filename }}
"""

import os
from typing import Optional, Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
{% if use_mcp %}
from pydantic_ai.mcp import MCP
{% endif %}

# Response Model
{{ response_model }}

# Agent-Konfiguration
def create_agent() -> Agent:
    """Erstelle und konfiguriere den Agent."""
    
    # LLM-Konfiguration
    llm_endpoint = {{ llm_endpoint|tojson }}
    llm_api_key = {{ llm_api_key|tojson }}
    llm_model_name = {{ llm_model|tojson }}
    
    print(f"Verbinde mit: {llm_endpoint}")
    print(f"Model: {llm_model_name}")
    
    # Provider und Model erstellen
    provider = OpenAIProvider(base_url=llm_endpoint, api_key=llm_api_key)
    model = OpenAIModel(provider=provider, model_name=llm_model_name)
    
    # System-Prompt
    system_prompt = {{ system_prompt|tojson }}
    
    # Agent erstellen
    agent = Agent(
        model=model,
        retries=3,
        system_prompt=system_prompt
    )
    
    return agent

{% if use_mcp %}
# MCP Server Integration (optional)
# Hier können MCP Server konfiguriert werden
{% endif %}

# Agent-Instanz
agent = create_agent()

# A2A-kompatible App erstellen
app = agent.to_a2a()

async def run_agent(user_input: str):
    """Führe den Agent mit Benutzereingabe aus."""
    try:
        result = await agent.run(user_input)
        
        # Verwende result.output statt result.data
        if hasattr(result, 'output'):
            return result.output
        elif hasattr(result, 'data'):
            return result.data
        else:
            return str(result)
            
    except Exception as e:
        return f"Entschuldigung, es gab einen Fehler: {str(e)}"

if __name__ == "__main__":
    import sys
    import uvicorn
    
    # Agent-Beschreibung als Variable
    agent_description = {{ description|tojson }}
    
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        print("🚀 Starte Agent als A2A Server...")
        print("Agent-Beschreibung:", agent_description)
        print("Server läuft auf: http://0.0.0.0:8000")
        print("Health Check: http://0.0.0.0:8000/health")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("🤖", agent_description)
        print("=" * 50)
        print("Interaktiver Modus - Geben Sie 'exit' zum Beenden ein")
        print("Für Server-Modus: python {{ filename }} server")
        print()
        
        import asyncio
        
        async def interactive_mode():
            while True:
                try:
                    user_input = input("Sie: ").strip()
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("Auf Wiedersehen! 👋")
                        break
                    
                    if user_input:
                        result = await run_agent(user_input)
                        print(f"Agent: {result}")
                        print()
                
                except KeyboardInterrupt:
                    print("\\nAuf Wiedersehen! 👋")
                    break
                except Exception as e:
                    print(f"Fehler: {e}\\n")
        
        asyncio.run(interactive_mode())
'''

    async def _generate_system_prompt_ai(self, description: str) -> str:
        """Verwende AI-Agent um optimalen System-Prompt zu generieren."""
        try:
            prompt_request = f"""Erstelle einen optimalen System-Prompt für einen AI-Agent basierend auf dieser Beschreibung:

"{description}"

Der System-Prompt soll den Agent perfekt für diese spezifische Aufgabe konfigurieren."""

            result = await self.prompt_engineer.run(prompt_request)

            if hasattr(result, "output"):
                return result.output
            elif hasattr(result, "data"):
                return result.data
            else:
                return str(result)

        except Exception as e:
            # Fallback auf einfachen Prompt
            return f"""Du bist ein spezialisierter AI-Agent.

Aufgabe: {description}

Führe deine Aufgabe professionell und präzise aus. Gib strukturierte, hilfreiche Antworten."""

    def _generate_system_prompt(self, description: str) -> str:
        """Generiere intelligenten System-Prompt mit AI-Agent."""
        import asyncio

        try:
            # Verwende AI-Agent für dynamische Prompt-Generierung
            return asyncio.run(self._generate_system_prompt_ai(description))
        except Exception as e:
            # Fallback falls AI-Agent nicht verfügbar
            return f"""Du bist ein spezialisierter AI-Agent.

Aufgabe: {description}

Führe deine Aufgabe professionell und präzise aus. Gib strukturierte, hilfreiche Antworten."""

    def _generate_response_model(self, description: str) -> str:
        """Generiere Pydantic Response Model basierend auf Beschreibung."""
        return '''class AgentResponse(BaseModel):
    """Response-Model für den generierten Agent."""
    
    response: str = Field(description="Die Hauptantwort des Agents")
    status: str = Field(default="success", description="Status der Ausführung")
    additional_info: Optional[dict] = Field(default=None, description="Zusätzliche Informationen")'''
        return '''class AgentResponse(BaseModel):
    """Response-Model für den generierten Agent."""
    
    response: str = Field(description="Die Hauptantwort des Agents")
    status: str = Field(default="success", description="Status der Ausführung")
    additional_info: Optional[dict] = Field(default=None, description="Zusätzliche Informationen")'''
