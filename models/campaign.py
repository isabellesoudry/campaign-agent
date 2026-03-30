from pydantic import BaseModel
from typing import List, Optional

class Segment(BaseModel):
    name: str
    criteria: str
    size: Optional[str] = None

class Deliverable(BaseModel):
    name: str
    channel: str
    subject_line: Optional[str] = None
    preview_text: Optional[str] = None
    body: Optional[str] = None
    cta: Optional[str] = None

class CampaignBrief(BaseModel):
    campaign_name: str
    objective: str
    launch_date: Optional[str] = None
    dri: Optional[str] = None
    segments: List[Segment] = []
    deliverables: List[Deliverable] = []
    compliance_flags: List[str] = []
    missing_fields: List[str] = []