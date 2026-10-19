# ROGERS-01 Full Starter Build

Local run:
1. Install Python 3.10+.
2. In this folder, run: `python -m venv .venv`
3. Activate it, then run: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open http://127.0.0.1:5000

Enable live AI:
- Set OPENAI_API_KEY as an environment variable on your machine or deployment host.
- Optional: set OPENAI_MODEL (defaults to gpt-4.1-mini).
- Never put API keys in HTML/JavaScript or commit them to GitHub.

Deploy to Render:
1. Create a GitHub repository and upload these project files.
2. In Render, create a new Blueprint from that repository, or create a Python web service.
3. Build command: pip install -r requirements.txt
4. Start command: `gunicorn app:app --workers 2 --threads 4 --timeout 120`
5. Add OPENAI_API_KEY in Render's Environment settings and deploy.
6. Test `/api/health` and the chat/file tools.

Implemented:
- Responsive dark command-center interface, Times New Roman, animated original geometric core
- Flask backend with live OpenAI chat endpoint when configured
- Browser speech recognition where supported, browser text-to-speech
- ATHENA / COMMANDER / TACTICAL response styles
- Text-based file analysis endpoint for TXT, MD, CSV, XML, HTML, PY, LOG
- Render deployment configuration

Not implemented yet:
- Deployment is not live until you connect your GitHub/Render accounts and set your secret API key.
- Browser speech synthesis is not voice cloning; custom cloned voices need a speech vendor integration.
- Persistent cloud memory, alarms/reminders, external web search, OAuth/login, PDF OCR, full DTD/XML schema validation and background tasks require additional work.
- Uploaded file contents are sent to the configured AI provider for analysis when live AI is enabled. Do not upload confidential client data unless your provider and deployment policies permit it.
