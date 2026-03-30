# Campaign Agent

A lifecycle marketing agent that evaluates your campaign brief for completeness 
and automatically generates a compliance approval deck — without manual formatting 
or copy-pasting.

---

## The Problem It Solves

Before a campaign can launch, marketers typically need to:
1. Manually check if the brief has all required fields
2. Build a compliance/bank approval deck by hand
3. Copy-paste copy from the brief into slides one by one

This agent does it in seconds.

---

## What It Does

**Step 1: Brief Evaluation**
Paste your raw campaign brief. The agent reads it and tells you:
- What fields were successfully extracted (objective, segments, deliverables, CTAs)
- What compliance flags were identified (eligibility rules, legal disclosures, experiment design)
- What's missing before you can proceed (DRI, launch date, body copy, etc.)
- A quality score out of 100

**Step 2: Compliance Deck Generation**
Once you're satisfied with the eval, download your auto-generated `.pptx` deck:
- Slide 1: Campaign name
- Slide 2: Overview, objective, launch date, DRI
- One slide per deliverable (Email, Push, House Ad) with extracted copy on the left and a Figma asset placeholder on the right

---

## In A Full Production Version

This simplified version outputs a `.pptx` file. In production, this pipeline would:
- Pull live Figma asset renders via Figma API using node IDs (as originally 
  built at Cash App)
- Push directly to Google Slides via API
- Auto-trigger when a new brief is added to a Google Drive folder
- Push generated ops tickets directly to Jira
- Use eval score trends to auto-improve extraction prompts over time

---

## Architecture
```
raw brief (text input)
↓
Agent 1: Brief Extractor
→ Claude reads unstructured brief
→ Returns structured CampaignBrief object
→ Flags missing required fields

↓
Agent 2: Output Generator
→ Takes structured CampaignBrief
→ Generates .pptx compliance deck
→ One slide per deliverable

↓
Agent 3: Eval Agent
→ Second Claude call acting as senior marketing reviewer
→ Scores extraction quality 0-100
→ Identifies gaps and compliance risks

↓
Logger
→ Saves every run to logs/pipeline_log.json
→ Tracks score trends over time
```

---

## Tech Stack

- **Python + FastAPI** — API framework
- **Anthropic Claude API** — brief extraction + evaluation
- **python-pptx** — deck generation
- **Pydantic** — data modeling and validation
- **Uvicorn** — ASGI server

---

## Project Structure
```
campaign-agent/
├── agents/
│   ├── brief_extractor.py     # Agent 1: reads brief, returns structured JSON
│   ├── output_generator.py    # Agent 2: generates .pptx deck
│   └── eval_agent.py          # Agent 3: scores output quality
├── models/
│   └── campaign.py            # Pydantic data models
├── context/
│   ├── brand-guidelines.md    # Brand context for agents
│   └── product-reference.md  # Product terminology reference
├── workflows/
│   └── campaign-brief-to-outputs.md  # End-to-end workflow definition
├── templates_html/
│   └── index.html             # Marketer-facing UI
├── main.py                    # FastAPI app + pipeline orchestration
└── AGENT.md                   # Master agent instructions
```

---

## Running Locally
```bash
# clone the repo
git clone https://github.com/isabellesoudry/campaign-agent
cd campaign-agent

# create virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# run the app
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Marketer-facing UI |
| POST | `/run-pipeline` | Run full agent pipeline on a brief |
| GET | `/download-deck` | Download generated .pptx deck |
| GET | `/docs` | Swagger API documentation |

---

## Eval Output Example
```json
{
  "score": 72,
  "passed": true,
  "strengths": [
    "Clear campaign objective with measurable goal",
    "Comprehensive compliance flags identified"
  ],
  "gaps": [
    "DRI missing — critical for accountability",
    "Launch date is vague — no specific date for scheduling",
    "Body copy missing for all deliverables"
  ],
  "recommendation": "Add DRI and specific launch date before campaign execution"
}
```

---

## Origin Story

This project is a direct evolution of two tools I built at Cash App:

**Campaign Automation Tool** — Google Apps Script + Figma API that extracted 
tagged content from marketing briefs to generate ops tickets, Jira compliance 
workflows, and bank review decks. Eliminated 4–6 hours of manual overhead per 
campaign.

**Internal MCP Repository** — Transformed unstructured campaign knowledge into 
machine-readable context, enabling AI agents to autonomously draft briefs, 
tickets, and results reports.

This project rebuilds that same workflow as a proper agentic pipeline — with 
evals, structured outputs, and a self-improving loop.
