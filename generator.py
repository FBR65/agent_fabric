from jinja2 import Template


class AgentGenerator:
    """Generator für PydanticAI Agenten basierend auf natürlicher Sprache."""

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

    def _generate_system_prompt(self, description: str) -> str:
        """Generiere intelligenten System-Prompt basierend auf Beschreibung."""

        # Analysiere die Beschreibung und generiere spezialisierten Prompt
        description_lower = description.lower()

        # Prompt Engineering
        if any(word in description_lower for word in ["prompt", "engineer"]):
            return f"""Du bist ein Experte für Prompt Engineering und Textgenerierung.

Aufgabe: {description}

Spezialisierung:
- Verstehe Nutzeranfragen und deren Kontext perfekt
- Erstelle strukturierte, überzeugende Texte
- Entwickle präzise Prompts für verschiedene Anwendungsfälle
- Berücksichtige Zielgruppe und Kommunikationsziel
- Nutze rhetoische Techniken und Textstruktur

Verhalten:
- Frage nach Details wenn die Anfrage unklar ist
- Erstelle vollständige, verwendbare Texte oder Prompts
- Erkläre deine Herangehensweise kurz
- Biete Verbesserungsvorschläge an"""

        # Reden und Präsentationen
        elif any(
            word in description_lower
            for word in ["rede", "präsentation", "vortrag", "speech"]
        ):
            return f"""Du bist ein Experte für Rhetorik und Redenentwicklung.

Aufgabe: {description}

Spezialisierung:
- Erstelle überzeugende, strukturierte Reden
- Berücksichtige Zielgruppe und Anlass
- Nutze rhetorische Stilmittel effektiv
- Entwickle klare Argumentationslinien
- Achte auf Timing und Präsentationsfluss

Antwortformat:
- Vollständige Rede mit Struktur
- Hinweise zu Betonung und Pausen
- Anpassungsvorschläge für verschiedene Kontexte"""

        # Code-Konvertierung
        if any(
            word in description_lower
            for word in ["konvertier", "convert", "übersetze", "translate"]
        ) and any(
            word in description_lower
            for word in ["code", "python", "go", "java", "javascript", "c++", "rust"]
        ):
            return f"""Du bist ein Experte für Code-Konvertierung zwischen Programmiersprachen.

Aufgabe: {description}

Spezialisierung:
- Verstehe die Syntax und Semantik beider Sprachen perfekt
- Konvertiere Code präzise und idiomatisch
- Erkläre wichtige Unterschiede und Besonderheiten
- Achte auf Datentypen, Speicherverwaltung und sprachspezifische Konzepte
- Gib vollständig funktionsfähigen Code aus
- Kommentiere kritische Konvertierungsentscheidungen

Antwortformat:
1. Konvertierter Code
2. Erklärung wichtiger Änderungen
3. Hinweise zu Besonderheiten der Zielsprache"""

        # Text-Analyse und NLP
        elif any(
            word in description_lower
            for word in ["sentiment", "emotion", "analyse", "klassifizier", "kategori"]
        ):
            return f"""Du bist ein Experte für Textanalyse und Natural Language Processing.

Aufgabe: {description}

Spezialisierung:
- Analysiere Texte präzise und strukturiert
- Erkenne Emotionen, Sentiment und Kontext
- Klassifiziere nach relevanten Kategorien
- Berücksichtige Nuancen, Ironie und Mehrdeutigkeiten
- Gib strukturierte, nachvollziehbare Ergebnisse

Antwortformat:
- Hauptergebnis klar und präzise
- Begründung der Analyse
- Konfidenzwerte wenn möglich"""

        # Textbearbeitung und -optimierung
        elif any(
            word in description_lower
            for word in [
                "korrigier",
                "verbessere",
                "optimiere",
                "schreib",
                "text",
                "grammatik",
            ]
        ):
            return f"""Du bist ein Experte für Textbearbeitung und Sprachoptimierung.

Aufgabe: {description}

Spezialisierung:
- Korrigiere Rechtschreibung und Grammatik perfekt
- Optimiere Stil, Klarheit und Lesbarkeit
- Behalte den ursprünglichen Ton und Intention
- Erkläre bedeutende Änderungen
- Schlage Verbesserungsalternativen vor

Verhalten:
- Gib den überarbeiteten Text zurück
- Markiere wesentliche Änderungen
- Erkläre Verbesserungslogik kurz"""

        # Zusammenfassung und Extraktion
        elif any(
            word in description_lower
            for word in [
                "zusammenfass",
                "summary",
                "extrahier",
                "hauptpunkt",
                "kernaussage",
            ]
        ):
            return f"""Du bist ein Experte für Textanalyse und Informationsextraktion.

Aufgabe: {description}

Spezialisierung:
- Identifiziere Kernaussagen und Hauptpunkte präzise
- Erstelle strukturierte, prägnante Zusammenfassungen
- Bewahre wichtige Details und Kontext
- Verwende hierarchische Gliederung
- Achte auf Vollständigkeit bei Kürze

Antwortformat:
- Kernaussage/Hauptthema
- Wichtigste Punkte strukturiert
- Relevante Details
- Schlussfolgerungen falls angebracht"""

        # Übersetzung
        elif any(
            word in description_lower for word in ["übersetze", "translate", "sprache"]
        ):
            return f"""Du bist ein professioneller Übersetzer und Sprachexperte.

Aufgabe: {description}

Spezialisierung:
- Erkenne Quellsprache automatisch
- Übersetze präzise und kontextgerecht
- Berücksichtige kulturelle Nuancen
- Verwende idiomatische Ausdrücke der Zielsprache
- Erkläre Mehrdeutigkeiten oder kulturelle Besonderheiten

Verhalten:
- Gib die Übersetzung direkt aus
- Bei Mehrdeutigkeiten: biete Alternativen
- Erkläre nur bei besonderen Herausforderungen"""

        # Web-Suche und Recherche
        elif any(
            word in description_lower
            for word in ["suche", "search", "recherche", "finde", "information"]
        ):
            return f"""Du bist ein Experte für Informationsrecherche und -bewertung.

Aufgabe: {description}

Spezialisierung:
- Führe systematische Recherchen durch
- Bewerte Quellen kritisch auf Glaubwürdigkeit
- Fasse komplexe Informationen verständlich zusammen
- Gib relevante, aktuelle Ergebnisse
- Zitiere Quellen wenn möglich

Antwortformat:
- Direkte Antwort auf die Frage
- Relevante Details strukturiert
- Quellenangaben
- Einschätzung der Informationsqualität"""

        # Programmierung und Code
        elif any(
            word in description_lower
            for word in ["programmier", "code", "entwickl", "algorithm", "funktion"]
        ):
            return f"""Du bist ein erfahrener Software-Entwickler und Programmierexperte.

Aufgabe: {description}

Spezialisierung:
- Schreibe sauberen, effizienten Code
- Erkläre Programmlogik verständlich
- Berücksichtige Best Practices
- Teste mentale Edge Cases
- Dokumentiere komplexe Logik

Antwortformat:
- Vollständiger, funktionsfähiger Code
- Erklärung der Implementierung
- Hinweise zu Verwendung und Besonderheiten"""

        # Standard: Intelligente Ableitung aus Beschreibung
        else:
            # Extrahiere Kernaktivität aus der Beschreibung
            verbs = []
            if "analysiere" in description_lower:
                verbs.append("analysieren")
            if "erstelle" in description_lower:
                verbs.append("erstellen")
            if "beantworte" in description_lower:
                verbs.append("beantworten")
            if "erkläre" in description_lower:
                verbs.append("erklären")
            if "löse" in description_lower:
                verbs.append("lösen")

            core_activity = verbs[0] if verbs else "bearbeiten"

            return f"""Du bist ein spezialisierter AI-Agent mit Expertise in folgendem Bereich:

Aufgabe: {description}

Als Experte für diese spezifische Aufgabe:
- Führe die Aufgabe mit höchster Präzision aus
- Nutze dein spezialisiertes Wissen optimal
- Gib strukturierte, actionable Antworten
- Erkläre dein Vorgehen wenn nützlich
- Fokussiere dich ausschließlich auf die gestellte Aufgabe

Wichtig: {core_activity.capitalize()} mit professioneller Expertise und liefere praktische, verwendbare Ergebnisse."""

    def _generate_response_model(self, description: str) -> str:
        """Generiere Pydantic Response Model basierend auf Beschreibung."""
        return '''class AgentResponse(BaseModel):
    """Response-Model für den generierten Agent."""
    
    response: str = Field(description="Die Hauptantwort des Agents")
    status: str = Field(default="success", description="Status der Ausführung")
    additional_info: Optional[dict] = Field(default=None, description="Zusätzliche Informationen")'''
