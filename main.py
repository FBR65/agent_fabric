#!/usr/bin/env python3
"""
Agent Fabric - Generiere Custom Agents aus umgangssprachlichen Beschreibungen
"""

import gradio as gr
import os
import logging
from pathlib import Path
from generator import AgentGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_agent_interface():
    """Erstelle die Gradio-Oberfläche für Agent Fabric."""

    generator = AgentGenerator()

    def generate_agent_code(
        description: str,
        use_mcp: bool,
        llm_endpoint: str,
        llm_api_key: str,
        llm_model: str,
    ):
        """Generiere Agent-Code basierend auf Beschreibung."""
        try:
            if not description.strip():
                return "", "❌ Bitte beschreiben Sie, was Ihr Agent können soll."

            code = generator.generate_agent(
                description=description,
                use_mcp=use_mcp,
                llm_endpoint=llm_endpoint,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                filename="mein_agent.py",
            )
            return code, "✅ Agent erfolgreich generiert!"
        except Exception as e:
            logger.error(f"Fehler bei der Agent-Generierung: {e}")
            return "", f"❌ Fehler: {str(e)}"

    def save_agent_code(code: str, filename: str):
        """Speichere den generierten Code in eine .py Datei."""
        if not code.strip():
            return "❌ Fehler: Kein Code zum Speichern vorhanden.", None, None

        if not filename.endswith(".py"):
            filename += ".py"

        try:
            # Agent-Code mit korrektem Dateinamen regenerieren
            import re

            updated_code = re.sub(
                r"python [^\.]*\.py server", f"python {filename} server", code
            )

            # Agent-Code speichern
            output_path = Path(filename)
            output_path.write_text(updated_code, encoding="utf-8")

            # requirements.txt im gleichen Verzeichnis erstellen
            req_path = output_path.parent / "requirements.txt"
            requirements_content = """# Dependencies für generierten Agent
pydantic-ai>=0.0.52
pydantic-ai-slim[a2a]>=0.0.52
fasta2a>=0.1.0
fastapi>=0.115.12
uvicorn>=0.34.0
httpx>=0.27.0
pydantic[email]>=2.11.3
"""
            req_path.write_text(requirements_content, encoding="utf-8")

            status_msg = f"✅ Agent gespeichert als: {output_path.absolute()}\n✅ Requirements erstellt: {req_path.absolute()}"

            # Return files for download
            return status_msg, str(output_path), str(req_path)
        except Exception as e:
            return f"❌ Fehler beim Speichern: {str(e)}", None, None

    # Gradio Interface
    with gr.Blocks(title="🤖 Agent Fabric", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 Agent Fabric")
        gr.Markdown("**Erstellen Sie KI-Agenten durch einfache Beschreibung**")

        with gr.Tabs():
            # Tab 1: Agent erstellen
            with gr.TabItem("🚀 Agent erstellen"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Was soll Ihr Agent können?")
                        description = gr.Textbox(
                            label="Agent-Beschreibung",
                            placeholder="Beschreiben Sie einfach, was Ihr Agent tun soll...\n\nBeispiele:\n• Texte korrigieren und verbessern\n• Sentiment von Nachrichten analysieren\n• Wetterinformationen abrufen\n• Nach Informationen im Web suchen",
                            lines=10,
                            max_lines=15,
                        )

                        use_mcp = gr.Checkbox(
                            label="🔧 Externe Tools nutzen (Web-Suche, Zeit, etc.)",
                            value=False,
                            info="Aktiviert den Zugriff auf externe Funktionen",
                        )

                        generate_btn = gr.Button(
                            "✨ Agent generieren", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### Generierter Code")
                        code_output = gr.Code(
                            label="Ihr Agent (ready to run)",
                            language="python",
                            lines=20,
                        )
                        status_output = gr.Textbox(label="Status", interactive=False)

                        with gr.Row():
                            filename_input = gr.Textbox(
                                label="Speichern als", value="mein_agent.py"
                            )
                            save_btn = gr.Button("💾 Speichern")

                        save_status = gr.Textbox(label="", interactive=False)

                        # Download Buttons
                        with gr.Row():
                            agent_download = gr.DownloadButton(
                                label="📥 Agent herunterladen", visible=False
                            )
                            requirements_download = gr.DownloadButton(
                                label="📥 Requirements herunterladen", visible=False
                            )

            # Tab 2: Erweiterte Einstellungen
            with gr.TabItem("⚙️ Einstellungen"):
                gr.Markdown("### LLM-Server Konfiguration")
                gr.Markdown(
                    "**Nur anpassen, wenn Sie einen eigenen LLM-Server verwenden**"
                )

                with gr.Row():
                    with gr.Column():
                        llm_endpoint = gr.Textbox(
                            label="Server-Adresse",
                            value="http://localhost:11434/v1",
                            info="Adresse Ihres LLM-Servers (z.B. Ollama, LM Studio)",
                        )
                        llm_model = gr.Textbox(
                            label="Model-Name",
                            value="qwen2.5:latest",
                            info="Name des verwendeten Modells",
                        )

                    with gr.Column():
                        llm_api_key = gr.Textbox(
                            label="API-Schlüssel",
                            value="sk-dummy",
                            type="password",
                            info="Nur bei kostenpflichtigen APIs erforderlich",
                        )

                        gr.Markdown("""
                        **Häufige Einstellungen:**
                        - **Ollama:** `http://localhost:11434/v1`
                        - **LM Studio:** `http://localhost:1234/v1`  
                        - **OpenAI:** `https://api.openai.com/v1`
                        """)

            # Tab 3: Beispiele
            with gr.TabItem("💡 Beispiele"):
                gr.Markdown("### Klicken Sie auf ein Beispiel, um es auszuprobieren")

                examples_list = [
                    ["Korrigiere deutsche Texte und verbessere die Grammatik", False],
                    [
                        "Analysiere die Stimmung von Kundenbewertungen und Social Media Posts",
                        False,
                    ],
                    [
                        "Suche nach aktuellen Nachrichten und Informationen im Internet",
                        True,
                    ],
                    ["Zeige mir die aktuelle Uhrzeit und das heutige Datum", True],
                    ["Hole Wetterinformationen für verschiedene Städte", True],
                    ["Übersetze Texte zwischen verschiedenen Sprachen", False],
                    ["Erstelle Zusammenfassungen von langen Texten", False],
                    ["Beantworte Fragen zu Programmierung und Code", False],
                ]

                for example_desc, example_mcp in examples_list:
                    with gr.Row():
                        gr.Button(f"📝 {example_desc}", variant="secondary").click(
                            lambda desc=example_desc, mcp=example_mcp: (desc, mcp),
                            outputs=[description, use_mcp],
                        )

            # Tab 4: Hilfe
            with gr.TabItem("❓ Hilfe"):
                gr.Markdown("""
                ## Wie funktioniert Agent Fabric?
                
                1. **Beschreiben Sie Ihren Agent** - Einfach in natürlicher Sprache
                2. **Agent wird generiert** - Automatisch als lauffähigen Python-Code
                3. **Code speichern** - Als .py Datei + requirements.txt
                4. **Dependencies installieren** - `pip install -r requirements.txt`
                5. **Agent verwenden** - Direkt ausführbar
                
                ## Installation der Dependencies
                
                **Mit pip:**
                ```bash
                pip install -r requirements.txt
                python mein_agent.py
                ```
                
                **Mit uv (empfohlen):**
                ```bash
                uv add pydantic-ai pydantic-ai-slim[a2a] fasta2a fastapi uvicorn
                python mein_agent.py
                ```
                
                ## Verwendung des generierten Agents
                
                ```bash
                # Agent interaktiv starten
                python mein_agent.py
                
                # Als Server starten (für andere Apps)
                python mein_agent.py server
                ```
                
                ## Was kann ein Agent?
                
                - **Texte bearbeiten:** Korrigieren, übersetzen, zusammenfassen
                - **Daten analysieren:** Sentiment-Analyse, Bewertungen auswerten  
                - **Informationen suchen:** Web-Suche, Fakten finden
                - **Funktionen ausführen:** Zeit, Wetter, Berechnungen
                
                ## Externe Tools
                
                Wenn Sie "Externe Tools nutzen" aktivieren, kann Ihr Agent:
                - Im Internet suchen
                - Aktuelle Zeit/Datum abrufen  
                - Wetterinformationen holen
                - Dateien bearbeiten
                
                **Hinweis:** Benötigt MCP-Server für erweiterte Funktionen
                """)

        # Event Handler (außerhalb der Tabs)
        generate_btn.click(
            generate_agent_code,
            inputs=[description, use_mcp, llm_endpoint, llm_api_key, llm_model],
            outputs=[code_output, status_output],
        )

        def handle_save_and_download(code, filename):
            """Handle save and show download buttons."""
            status, agent_path, req_path = save_agent_code(code, filename)

            if agent_path and req_path:
                return (
                    status,
                    gr.DownloadButton(
                        label="📥 Agent herunterladen", value=agent_path, visible=True
                    ),
                    gr.DownloadButton(
                        label="📥 Requirements herunterladen",
                        value=req_path,
                        visible=True,
                    ),
                )
            else:
                return (
                    status,
                    gr.DownloadButton(visible=False),
                    gr.DownloadButton(visible=False),
                )

        save_btn.click(
            handle_save_and_download,
            inputs=[code_output, filename_input],
            outputs=[save_status, agent_download, requirements_download],
        )

    return interface


def main():
    """Starte die Agent Fabric Anwendung."""
    host = os.getenv("GRADIO_HOST", "127.0.0.1")
    port = int(os.getenv("GRADIO_PORT", "7860"))

    logger.info(f"🚀 Agent Fabric startet auf {host}:{port}")

    interface = create_agent_interface()
    interface.launch(
        server_name=host, server_port=port, share=False, debug=False, show_error=True
    )


if __name__ == "__main__":
    main()
