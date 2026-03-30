# Campaign Agent — Master Instructions

## What This Agent Does
This agent takes a raw marketing campaign brief and autonomously:
1. Extracts all structured fields from unstructured text
2. Evaluates brief completeness and flags what's missing
3. Generates a compliance approval deck ready for bank/legal review

## Agent Roles

### Agent 1: Brief Extractor (`agents/brief_extractor.py`)
- Reads raw brief text
- Extracts: campaign name, objective, launch date, DRI, segments, deliverables, compliance flags
- Flags any missing required fields
- Returns structured `CampaignBrief` object

### Agent 2: Output Generator (`agents/output_generator.py`)
- Takes structured `CampaignBrief`
- Generates `.pptx` compliance deck
- Slide 1: Campaign name
- Slide 2: Overview, objective, launch date, DRI, segments, compliance flags
- Slides 3+: One per deliverable with extracted copy + Figma asset placeholder

### Agent 3: Eval Agent (`agents/eval_agent.py`)
- Acts as a senior lifecycle marketing reviewer
- Scores extraction quality 0-100
- Identifies gaps that would block campaign execution
- Flags compliance risks
- Logs result for trend tracking

## Input Format
Raw marketing brief text containing any of:
- Campaign name and objective
- Launch date and DRI
- Audience segments with eligibility criteria
- Deliverables (Email, Push, House Ad) with copy
- Compliance requirements

## Output Format
- Structured JSON campaign object
- `.pptx` compliance deck
- Eval score + gap analysis
- Run log entry in `logs/pipeline_log.json`

## Quality Standards
- All required fields must be present or explicitly flagged as missing
- Compliance flags must be called out before deck generation
- Eval agent must score every output before it is returned
- Every run must be logged for trend tracking

## Context
See `/context` folder for brand guidelines and product reference.

## Workflows
See `/workflows` folder for end-to-end process documentation.