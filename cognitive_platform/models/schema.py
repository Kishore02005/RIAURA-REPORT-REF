from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Domain System
# ---------------------------------------------------------------------------

class CognitiveDomainName(str, Enum):
    ATTENTION = "attention"
    MEMORY = "memory"
    PROCESSING = "processing"
    REASONING = "reasoning"
    DECISION_INTEGRITY = "decision_integrity"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    ORIGINALITY = "originality"
    METACOGNITION = "metacognition"


# AHIMS domain color system — single source of truth
DOMAIN_SEMANTIC_COLORS: dict[CognitiveDomainName, str] = {
    CognitiveDomainName.ATTENTION: "#F5A623",
    CognitiveDomainName.MEMORY: "#1F9E96",
    CognitiveDomainName.PROCESSING: "#3D63DD",
    CognitiveDomainName.REASONING: "#7C5CFC",
    CognitiveDomainName.DECISION_INTEGRITY: "#2E8B57",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "#E8607A",
    CognitiveDomainName.ORIGINALITY: "#F0654A",
    CognitiveDomainName.METACOGNITION: "#4B3F72",
}

DOMAIN_DISPLAY_NAMES: dict[CognitiveDomainName, str] = {
    CognitiveDomainName.ATTENTION: "Attention",
    CognitiveDomainName.MEMORY: "Memory",
    CognitiveDomainName.PROCESSING: "Processing Speed",
    CognitiveDomainName.REASONING: "Reasoning",
    CognitiveDomainName.DECISION_INTEGRITY: "Decision Integrity",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "Emotional Intelligence",
    CognitiveDomainName.ORIGINALITY: "Originality",
    CognitiveDomainName.METACOGNITION: "Metacognition",
}

DOMAIN_BRAIN_REGIONS: dict[CognitiveDomainName, str] = {
    CognitiveDomainName.ATTENTION: "Prefrontal Cortex & Parietal Lobe",
    CognitiveDomainName.MEMORY: "Hippocampus & Temporal Lobe",
    CognitiveDomainName.PROCESSING: "Basal Ganglia & White Matter Tracts",
    CognitiveDomainName.REASONING: "Dorsolateral Prefrontal Cortex",
    CognitiveDomainName.DECISION_INTEGRITY: "Anterior Cingulate & Ventromedial PFC",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "Insula & Amygdala Complex",
    CognitiveDomainName.ORIGINALITY: "Default Mode Network & Temporal Poles",
    CognitiveDomainName.METACOGNITION: "Frontopolar Cortex & Medial PFC",
}

DOMAIN_SHORT_DESCRIPTIONS: dict[CognitiveDomainName, str] = {
    CognitiveDomainName.ATTENTION: "The capacity to sustain, select, and allocate cognitive resources to relevant stimuli over time.",
    CognitiveDomainName.MEMORY: "The ability to encode, consolidate, and retrieve information across short and long-term storage systems.",
    CognitiveDomainName.PROCESSING: "The speed and efficiency at which cognitive operations are executed without sacrificing accuracy.",
    CognitiveDomainName.REASONING: "The capacity to construct, evaluate, and apply logical frameworks to novel and familiar problems.",
    CognitiveDomainName.DECISION_INTEGRITY: "The consistency between internalized values and behavioral choices under varying cognitive loads.",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "The perception, interpretation, and regulation of emotional information in self and others.",
    CognitiveDomainName.ORIGINALITY: "The ability to generate diverse, novel, and useful ideas across different problem contexts.",
    CognitiveDomainName.METACOGNITION: "The awareness and regulation of one's own thinking processes and strategy selection.",
}


# ---------------------------------------------------------------------------
# Input schemas
# ---------------------------------------------------------------------------

class Metadata(BaseModel):
    company_logo: str = Field(default="/static/assets/riaura-logo.svg")
    company_name: str = Field(default="Riaura")
    participant_name: str
    age: int = Field(..., ge=10, le=100)
    gender: str
    assessment_date: date
    assessment_id: Optional[str] = None


class CognitiveDomain(BaseModel):
    name: CognitiveDomainName
    score: float = Field(..., ge=0, le=100)


class AssessmentData(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    domains: list[CognitiveDomain]


class PsychometricReport(BaseModel):
    metadata: Metadata
    assessment: AssessmentData
    brain_mapping_asset: str = Field(default="/static/assets/brain-placeholder.svg")


# ---------------------------------------------------------------------------
# Processed report schemas — one per page
# ---------------------------------------------------------------------------

class PerformanceTier(str, Enum):
    DISTINGUISHED = "distinguished"
    HIGH = "high"
    MODERATE = "moderate"
    DEVELOPING = "developing"


# Page 2 — Participant Overview
class HighlightBadge(BaseModel):
    label: str
    value: str
    color: str


# Page 3 — Executive Summary
class ExecutiveInsight(BaseModel):
    title: str
    body: str


class ExecutiveSummary(BaseModel):
    narrative: str
    insights: list[ExecutiveInsight]
    closing_takeaway: str


# Page 4 — Performance Dashboard
class PerformanceOverview(BaseModel):
    summary_statement: str
    overall_score: float
    overall_tier: PerformanceTier
    domain_interpretations: list[DomainInterpretation]
    constellation_data: dict
    interpretation_callout: str


# Page 5 — Functional Brain Associations
class FunctionalBrainAssociation(BaseModel):
    domain: CognitiveDomainName
    display_name: str
    color: str
    brain_region: str
    functional_role: str
    association_note: str


# Page 6 — Domain Matrix
class DomainCard(BaseModel):
    domain: CognitiveDomainName
    display_name: str
    score: float
    tier: PerformanceTier
    color: str
    short_description: str
    interpretation: str


# Page 7 — Pattern Analysis
class PatternInsight(BaseModel):
    title: str
    description: str
    domains_involved: list[str]
    significance: str


# Page 8 — Persona
class CognitivePersona(BaseModel):
    title: str
    descriptor: str
    narrative: str
    trait_tags: list[str]
    persona_motif: str


# Page 9 — Interpersonal Insights
class InterpersonalInsight(BaseModel):
    title: str
    category: str
    description: str
    communication_cues: list[str]


# Page 10 — Development Strategy
class DevelopmentStage(BaseModel):
    stage: str
    focus_area: str
    description: str
    priority: str
    actions: list[str]


# Page 11 — Recommended Labs
class RecommendedLab(BaseModel):
    rank: int
    domain: CognitiveDomainName
    display_name: str
    color: str
    title: str
    description: str
    lab_name: str
    lab_description: str
    rationale: str


# Page 12 — Methodology
class MethodologySection(BaseModel):
    title: str
    content: str


# Shared
class DomainInterpretation(BaseModel):
    domain: CognitiveDomainName
    display_name: str
    score: float
    tier: PerformanceTier
    color: str
    brain_region: str
    narrative: str
    micro_insight: str
    functional_behavior: str


# ---------------------------------------------------------------------------
# Full processed report
# ---------------------------------------------------------------------------

class ProcessedReport(BaseModel):
    metadata: Metadata
    assessment: AssessmentData
    brain_mapping_asset: str

    # Page 1 — Cover
    cover_tagline: str

    # Page 2 — Participant Overview
    highlight_badges: list[HighlightBadge]
    overview_summary: str

    # Page 3 — Executive Summary
    executive_summary: ExecutiveSummary

    # Page 4 — Performance Dashboard
    performance_overview: PerformanceOverview

    # Page 5 — Functional Brain Associations
    brain_associations: list[FunctionalBrainAssociation]

    # Page 6 — Domain Matrix
    domain_cards: list[DomainCard]

    # Page 7 — Pattern Analysis
    pattern_insights: list[PatternInsight]
    pattern_summary: str

    # Page 8 — Persona
    persona: CognitivePersona

    # Page 9 — Interpersonal Insights
    interpersonal_insights: list[InterpersonalInsight]

    # Page 10 — Development Strategy
    development_stages: list[DevelopmentStage]

    # Page 11 — Recommended Labs
    recommended_labs: list[RecommendedLab]

    # Page 12 — Methodology
    methodology_sections: list[MethodologySection]

    # Page 13 — Back Cover
    closing_statement: str
    closing_tagline: str

    # Chart data
    constellation_chart_data: dict
    radar_chart_data: dict
    parallel_coordinates_data: dict
