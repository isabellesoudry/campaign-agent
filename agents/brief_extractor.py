import os
import json
import anthropic
from dotenv import load_dotenv
from models.campaign import CampaignBrief, Segment, Deliverable

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def clean_json_response(text):
    text = text.strip()
    # remove markdown code fences
    if "```" in text:
        # extract content between first ``` and last ```
        parts = text.split("```")
        # parts[1] is the content between first pair of ```
        if len(parts) >= 3:
            text = parts[1]
        # remove language identifier like "json"
        if text.startswith("json"):
            text = text[4:]
    # find the first { and last } to extract just the JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end+1]
    return text.strip()

def extract_brief(brief_text: str) -> CampaignBrief:

    template = """
{
    "campaign_name": "name of the campaign",
    "objective": "the campaign objective",
    "launch_date": "launch date or null",
    "dri": "directly responsible individual or null",
    "segments": [
        {
            "name": "segment name",
            "criteria": "eligibility criteria",
            "size": "estimated size or null"
        }
    ],
    "deliverables": [
        {
            "name": "deliverable name e.g. Email 1 - Day 7",
            "channel": "email, push, or house ad",
            "subject_line": "subject line or null",
            "preview_text": "preview text or null",
            "body": "full body copy or null",
            "cta": "call to action text or null"
        }
    ],
    "compliance_flags": ["list of any compliance or legal items flagged"],
    "missing_fields": ["list any required fields that were missing"]
}"""

    prompt = (
        "You are a lifecycle marketing expert. Read the following campaign brief "
        "and extract all relevant information into a structured JSON object.\n\n"
        "Return ONLY valid JSON, no other text. Use this exact structure:\n"
        + template
        + "\n\nCampaign Brief:\n"
        + brief_text
    )

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = clean_json_response(message.content[0].text)
    data = json.loads(response_text)

    segments = [Segment(**s) for s in data.get("segments", [])]
    deliverables = [Deliverable(**d) for d in data.get("deliverables", [])]

    return CampaignBrief(
        campaign_name=data["campaign_name"],
        objective=data["objective"],
        launch_date=data.get("launch_date"),
        dri=data.get("dri"),
        segments=segments,
        deliverables=deliverables,
        compliance_flags=data.get("compliance_flags", []),
        missing_fields=data.get("missing_fields", [])
    )