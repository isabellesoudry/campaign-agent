import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.brief_extractor import extract_brief
from agents.output_generator import generate_deck
from agents.eval_agent import evaluate_brief

app = FastAPI(
    title="Campaign Agent",
    description="Automatically generates campaign decks from raw marketing briefs",
    version="1.0.0"
)

class BriefInput(BaseModel):
    brief_text: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates_html/index.html", "r") as f:
        return f.read()

@app.post("/run-pipeline")
def run_pipeline(input: BriefInput):
    try:
        print("📋 Step 1: Extracting brief...")
        brief = extract_brief(input.brief_text)
        
        print("📊 Step 2: Generating deck...")
        deck_path = generate_deck(brief)
        
        print("🔍 Step 3: Evaluating outputs...")
        eval_result = evaluate_brief(brief)
        
        print("💾 Step 4: Logging result...")
        log_result(brief, eval_result)
        
        return {
            "status": "success",
            "campaign_name": brief.campaign_name,
            "deliverables_found": len(brief.deliverables),
            "segments_found": len(brief.segments),
            "compliance_flags": brief.compliance_flags,
            "missing_fields": brief.missing_fields,
            "eval_score": eval_result["score"],
            "eval_passed": eval_result["passed"],
            "eval_gaps": eval_result["gaps"],
            "deck_path": deck_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-deck")
def download_deck():
    path = "output/campaign_deck.pptx"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="No deck found. Run the pipeline first.")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="campaign_deck.pptx"
    )

def log_result(brief, eval_result):
    os.makedirs("logs", exist_ok=True)
    log = {
        "campaign_name": brief.campaign_name,
        "deliverables": len(brief.deliverables),
        "eval_score": eval_result["score"],
        "eval_passed": eval_result["passed"],
        "gaps": eval_result["gaps"]
    }
    log_file = "logs/pipeline_log.json"
    history = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            history = json.load(f)
    history.append(log)
    with open(log_file, "w") as f:
        json.dump(history, f, indent=2)