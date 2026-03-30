import os
import json
import anthropic
from dotenv import load_dotenv
from models.campaign import CampaignBrief

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def clean_json_response(text):
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end+1]
    return text.strip()

def evaluate_brief(brief: CampaignBrief) -> dict:

    brief_summary = (
        f"Campaign Name: {brief.campaign_name}\n"
        f"Objective: {brief.objective}\n"
        f"Launch Date: {brief.launch_date or 'missing'}\n"
        f"DRI: {brief.dri or 'missing'}\n"
        f"Segments: {len(brief.segments)} segment(s)\n"
        f"Deliverables: {len(brief.deliverables)} deliverable(s)\n"
        f"Compliance Flags: {brief.compliance_flags or 'none identified'}\n"
        f"Missing Fields: {brief.missing_fields or 'none'}\n\n"
        "Deliverables extracted:\n" +
        "\n".join([
            f"- {d.name} ({d.channel}): SL={d.subject_line}, CTA={d.cta}"
            for d in brief.deliverables
        ])
    )

    prompt = (
        "You are a senior lifecycle marketing manager reviewing an automatically extracted campaign brief.\n\n"
        "Score this extraction on a scale of 0-100 and provide feedback.\n\n"
        "Evaluate based on:\n"
        "- Are all key campaign fields present? (objective, launch date, DRI)\n"
        "- Are segments clearly defined with criteria?\n"
        "- Do all deliverables have subject lines, body copy, and CTAs?\n"
        "- Are compliance flags identified?\n"
        "- What is missing or unclear?\n\n"
        "Return ONLY valid JSON, no markdown, no backticks, just raw JSON:\n"
        "{\n"
        '    "score": 85,\n'
        '    "passed": true,\n'
        '    "strengths": ["list of things extracted well"],\n'
        '    "gaps": ["list of missing or unclear items"],\n'
        '    "recommendation": "one sentence on what to fix"\n'
        "}\n\n"
        "Brief extraction to evaluate:\n"
        + brief_summary
    )

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = message.content[0].text
    print("RAW EVAL RESPONSE:", raw[:300])
    cleaned = clean_json_response(raw)
    result = json.loads(cleaned)
    return result