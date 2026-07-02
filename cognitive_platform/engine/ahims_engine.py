"""AHIMS Cognitive Engine — generates all narrative content for the 13-section scroll report."""
from __future__ import annotations

import json
import math
from typing import Any

from models.schema import (
    AssessmentData,
    CognitiveDomain,
    CognitiveDomainName,
    DOMAIN_BRAIN_REGIONS,
    DOMAIN_DISPLAY_NAMES,
    DOMAIN_SEMANTIC_COLORS,
    DOMAIN_SHORT_DESCRIPTIONS,
    Metadata,
    PerformanceTier,
    PsychometricReport,
)


# ---------------------------------------------------------------------------
# Domain mapping for AHIMS color system
# ---------------------------------------------------------------------------

AHIMS_COLORS = {
    CognitiveDomainName.ATTENTION: "#F5A623",
    CognitiveDomainName.MEMORY: "#1F9E96",
    CognitiveDomainName.PROCESSING: "#3D63DD",
    CognitiveDomainName.REASONING: "#7C5CFC",
    CognitiveDomainName.DECISION_INTEGRITY: "#2E8B57",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "#E8607A",
    CognitiveDomainName.ORIGINALITY: "#F0654A",
    CognitiveDomainName.METACOGNITION: "#4B3F72",
}

DOMAIN_ICONS = {
    CognitiveDomainName.ATTENTION: "eye",
    CognitiveDomainName.MEMORY: "database",
    CognitiveDomainName.PROCESSING: "zap",
    CognitiveDomainName.REASONING: "cpu",
    CognitiveDomainName.DECISION_INTEGRITY: "shield",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "heart",
    CognitiveDomainName.ORIGINALITY: "sparkles",
    CognitiveDomainName.METACOGNITION: "brain",
}

TIER_THRESHOLDS = [
    (85, PerformanceTier.DISTINGUISHED, "Highly Developed"),
    (70, PerformanceTier.HIGH, "Well Developed"),
    (50, PerformanceTier.MODERATE, "Balanced Profile"),
    (0, PerformanceTier.DEVELOPING, "Emerging Capacity"),
]

TIER_NARRATIVES = {
    PerformanceTier.DISTINGUISHED: "Your results indicate a level of cognitive engagement that exceeds normative benchmarks. This pattern suggests particularly efficient neural architecture.",
    PerformanceTier.HIGH: "You demonstrate a strong capacity in this area, performing above the central tendency of the reference population.",
    PerformanceTier.MODERATE: "Your performance falls within the expected range for the general population, indicating a stable cognitive foundation.",
    PerformanceTier.DEVELOPING: "Your results suggest this domain presents an area where targeted engagement may yield meaningful improvement.",
}

BEHAVIORS = {
    CognitiveDomainName.ATTENTION: {
        PerformanceTier.DISTINGUISHED: "Maintaining focused concentration across extended tasks with minimal distraction interference.",
        PerformanceTier.HIGH: "Filtering distractors effectively in moderately complex environments.",
        PerformanceTier.MODERATE: "Sustaining attention for standard-duration tasks with occasional variability.",
        PerformanceTier.DEVELOPING: "Benefiting from structured cueing in complex attentional settings.",
    },
    CognitiveDomainName.MEMORY: {
        PerformanceTier.DISTINGUISHED: "Consolidating and retrieving information with high fidelity across delays.",
        PerformanceTier.HIGH: "Retaining and recalling structured information reliably.",
        PerformanceTier.MODERATE: "Encoding and retrieving information at expected rates.",
        PerformanceTier.DEVELOPING: "Benefiting from repetition and multi-modal encoding strategies.",
    },
    CognitiveDomainName.PROCESSING: {
        PerformanceTier.DISTINGUISHED: "Executing rapid cognitive operations without accuracy trade-offs.",
        PerformanceTier.HIGH: "Completing sequential and parallel processing tasks efficiently.",
        PerformanceTier.MODERATE: "Processing information at a steady, functional pace.",
        PerformanceTier.DEVELOPING: "Showing throughput that may improve with targeted practice.",
    },
    CognitiveDomainName.REASONING: {
        PerformanceTier.DISTINGUISHED: "Applying abstract rules flexibly across novel problem spaces.",
        PerformanceTier.HIGH: "Solving deductive and inductive problems with consistent accuracy.",
        PerformanceTier.MODERATE: "Reasoning effectively within familiar logical frameworks.",
        PerformanceTier.DEVELOPING: "Developing capacity for abstract and relational reasoning.",
    },
    CognitiveDomainName.DECISION_INTEGRITY: {
        PerformanceTier.DISTINGUISHED: "Making decisions that reflect strong consistency with internalized values under pressure.",
        PerformanceTier.HIGH: "Maintaining decision coherence across varying cognitive loads.",
        PerformanceTier.MODERATE: "Making sound decisions under typical conditions.",
        PerformanceTier.DEVELOPING: "Benefiting from structured decision frameworks under ambiguity.",
    },
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: {
        PerformanceTier.DISTINGUISHED: "Perceiving, interpreting, and regulating emotional information with nuance.",
        PerformanceTier.HIGH: "Demonstrating strong awareness of emotional cues in self and others.",
        PerformanceTier.MODERATE: "Responding to emotional information at expected social-cognitive levels.",
        PerformanceTier.DEVELOPING: "Building capacity for emotional perception and regulation.",
    },
    CognitiveDomainName.ORIGINALITY: {
        PerformanceTier.DISTINGUISHED: "Generating diverse, original solutions with fluency and flexibility.",
        PerformanceTier.HIGH: "Applying creative thinking across unfamiliar problem contexts.",
        PerformanceTier.MODERATE: "Producing conventional solutions with occasional novel approaches.",
        PerformanceTier.DEVELOPING: "Developing divergent ideation capacity.",
    },
    CognitiveDomainName.METACOGNITION: {
        PerformanceTier.DISTINGUISHED: "Accurately monitoring your own cognitive processes and adjusting strategies proactively.",
        PerformanceTier.HIGH: "Self-regulating effectively and selecting appropriate strategies.",
        PerformanceTier.MODERATE: "Demonstrating standard self-awareness of cognitive strengths.",
        PerformanceTier.DEVELOPING: "Developing awareness of your own thinking processes.",
    },
}

DEVELOPMENT_HINTS = {
    CognitiveDomainName.ATTENTION: "Try timed focus sessions with gradual duration increases. Minimize multitasking during deep work.",
    CognitiveDomainName.MEMORY: "Use spaced repetition and multi-sensory encoding. Connect new information to existing knowledge.",
    CognitiveDomainName.PROCESSING: "Practice speed-accuracy trade-off exercises. Start with simple stimuli and increase complexity.",
    CognitiveDomainName.REASONING: "Engage with abstract puzzles and logical frameworks. Practice identifying patterns in unfamiliar data.",
    CognitiveDomainName.DECISION_INTEGRITY: "Reflect on values before making decisions. Practice decision-making under low-stakes conditions.",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "Practice emotional labeling and perspective-taking. Seek feedback on interpersonal dynamics.",
    CognitiveDomainName.ORIGINALITY: "Generate multiple solutions before selecting one. Explore unfamiliar domains for cross-pollination.",
    CognitiveDomainName.METACOGNITION: "Keep a thinking journal. Before tasks, state your strategy; after, evaluate what worked.",
}

FUNCTIONAL_INSIGHTS_DATA = [
    {
        "title": "Learning & Knowledge Acquisition",
        "icon": "book-open",
        "description": "How you absorb, process, and retain new information.",
        "domains": ["Memory", "Attention", "Processing"],
        "narrative": "Your memory and attention systems work together to determine how effectively you encode and retain new information. Strong performance here means knowledge sticks.",
    },
    {
        "title": "Decision Making Under Pressure",
        "icon": "target",
        "description": "How you make choices when stakes are high.",
        "domains": ["Decision Integrity", "Reasoning", "Metacognition"],
        "narrative": "Decision integrity combined with reasoning determines the quality of your choices. Metacognition provides the self-awareness to know when you need more information.",
    },
    {
        "title": "Adaptability & Flexibility",
        "icon": "refresh-cw",
        "description": "How you respond to change and novelty.",
        "domains": ["Processing", "Originality", "Metacognition"],
        "narrative": "Processing speed enables rapid adaptation, while originality generates novel responses. Metacognition helps you recognize when your current approach isn't working.",
    },
    {
        "title": "Sustained Focus & Concentration",
        "icon": "focus",
        "description": "How you maintain attention over extended periods.",
        "domains": ["Attention", "Metacognition", "Memory"],
        "narrative": "Attention is the gateway for all cognitive processing. When sustained, it allows deep engagement with complex tasks and information.",
    },
    {
        "title": "Creative Problem Solving",
        "icon": "lightbulb",
        "description": "How you generate and evaluate novel solutions.",
        "domains": ["Originality", "Reasoning", "Processing"],
        "narrative": "Originality generates divergent ideas, reasoning evaluates them logically, and processing speed determines how quickly you can iterate through solutions.",
    },
    {
        "title": "Planning & Organization",
        "icon": "calendar",
        "description": "How you structure tasks and manage complexity.",
        "domains": ["Metacognition", "Reasoning", "Attention"],
        "narrative": "Metacognition provides the self-awareness to plan effectively, reasoning structures the plan logically, and attention ensures follow-through.",
    },
]

INTERPERSONAL_CONNECTIONS = [
    {"skill": "Communication", "domains": ["Emotional Intelligence", "Reasoning"], "description": "How clearly you express ideas and listen to others."},
    {"skill": "Collaboration", "domains": ["Emotional Intelligence", "Metacognition"], "description": "How effectively you work with diverse teams."},
    {"skill": "Emotional Awareness", "domains": ["Emotional Intelligence", "Attention"], "description": "How accurately you perceive emotional cues in yourself and others."},
    {"skill": "Conflict Navigation", "domains": ["Decision Integrity", "Emotional Intelligence"], "description": "How you handle disagreements and find resolution."},
    {"skill": "Team Contribution", "domains": ["Processing", "Originality", "Reasoning"], "description": "What unique value you bring to group work."},
]

BALANCE_DESCRIPTIONS = {
    "high": "Your cognitive profile shows strong balance across domains, suggesting a versatile and adaptable cognitive architecture.",
    "moderate": "Your profile shows moderate variation, with clear strengths that complement developing areas.",
    "low": "Your profile is highly differentiated, with pronounced strengths alongside areas for growth.",
}


def _tier(score: float) -> PerformanceTier:
    for threshold, tier, _ in TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    return PerformanceTier.DEVELOPING


def _tier_label(score: float) -> str:
    for threshold, _, label in TIER_THRESHOLDS:
        if score >= threshold:
            return label
    return "Emerging Capacity"


def _balance_score(assessment: AssessmentData) -> float:
    scores = [d.score for d in assessment.domains]
    avg = sum(scores) / len(scores)
    variance = sum((s - avg) ** 2 for s in scores) / len(scores)
    std_dev = math.sqrt(variance)
    return max(0, min(100, 100 - std_dev * 2))


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _build_section2_overview(assessment: AssessmentData) -> dict[str, Any]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    return {
        "transition_sentence": "Your cognitive profile is built from eight interconnected domains.",
        "overall_score": assessment.overall_score,
        "tier_label": _tier_label(assessment.overall_score),
        "domain_preview": [
            {"name": DOMAIN_DISPLAY_NAMES[d.name], "score": d.score, "color": AHIMS_COLORS[d.name]}
            for d in sorted_d
        ],
    }


def _build_section3_executive(assessment: AssessmentData) -> dict[str, Any]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    top = sorted_d[0]
    bottom = sorted_d[-1]
    scores = [d.score for d in assessment.domains]
    spread = max(scores) - min(scores)
    avg = sum(scores) / len(scores)

    if spread <= 15:
        style = "Versatile Generalist"
        style_desc = "You demonstrate broadly balanced cognitive capabilities, suggesting adaptability across diverse task demands."
    elif spread <= 25:
        style = "Focused Specialist"
        style_desc = "You show clear cognitive strengths that you apply with depth, complemented by developing capabilities."
    else:
        style = "Distinctive Profile"
        style_desc = "You possess a highly differentiated cognitive architecture with pronounced peaks and valleys."

    confidence = "High" if all(s > 40 for s in scores) else "Moderate" if all(s > 25 for s in scores) else "Variable"

    return {
        "pull_quote": (
            f"Your cognitive profile reveals a distinctive pattern anchored in "
            f"{DOMAIN_DISPLAY_NAMES[top.name].lower()}, creating a unique "
            f"architecture of cognitive strengths."
        ),
        "paragraphs": [
            f"Across eight assessed cognitive domains, your profile demonstrates a {'broadly elevated' if assessment.overall_score >= 75 else 'differentiated'} pattern of performance. Your highest capacity is observed in {DOMAIN_DISPLAY_NAMES[top.name]} ({top.score:.0f}%), while {DOMAIN_DISPLAY_NAMES[bottom.name]} ({bottom.score:.0f}%) represents the area with the most room for development.",
            f"The spread across your domains is {spread:.0f} percentage points, {'indicating a well-balanced cognitive profile' if spread <= 20 else 'reflecting a differentiated profile with distinct cognitive strengths'}. This pattern reflects how your cognitive systems are currently organized and integrated.",
        ],
        "strongest_capability": {
            "name": DOMAIN_DISPLAY_NAMES[top.name],
            "score": top.score,
            "color": AHIMS_COLORS[top.name],
            "narrative": TIER_NARRATIVES[_tier(top.score)],
        },
        "primary_development": {
            "name": DOMAIN_DISPLAY_NAMES[bottom.name],
            "score": bottom.score,
            "color": AHIMS_COLORS[bottom.name],
            "narrative": TIER_NARRATIVES[_tier(bottom.score)],
        },
        "overall_style": {"name": style, "description": style_desc},
        "confidence_note": f"Confidence level: {confidence}. {'All domain scores are above 40%, indicating reliable measurement across the board.' if confidence == 'High' else 'Some domain scores suggest measurement variability. Consider re-assessment for domains below 40%.' if confidence == 'Variable' else 'Most domain scores are above 25%, providing a reasonable overall picture.'}",
    }


def _build_section4_performance(assessment: AssessmentData) -> dict[str, Any]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    b = _balance_score(assessment)
    if b >= 80:
        balance_level = "high"
    elif b >= 50:
        balance_level = "moderate"
    else:
        balance_level = "low"

    return {
        "domain_ranking": [
            {"name": DOMAIN_DISPLAY_NAMES[d.name], "score": d.score, "color": AHIMS_COLORS[d.name], "brain_region": DOMAIN_BRAIN_REGIONS[d.name]}
            for d in sorted_d
        ],
        "balance_score": round(b, 1),
        "balance_description": BALANCE_DESCRIPTIONS[balance_level],
        "avg_score": round(sum(d.score for d in assessment.domains) / len(assessment.domains), 1),
    }


def _build_section5_explorer(assessment: AssessmentData) -> list[dict[str, Any]]:
    result = []
    for d in assessment.domains:
        t = _tier(d.score)
        result.append({
            "name": DOMAIN_DISPLAY_NAMES[d.name],
            "key": d.name.value,
            "score": d.score,
            "color": AHIMS_COLORS[d.name],
            "icon": DOMAIN_ICONS[d.name],
            "brain_region": DOMAIN_BRAIN_REGIONS[d.name],
            "description": DOMAIN_SHORT_DESCRIPTIONS[d.name],
            "narrative": TIER_NARRATIVES[t],
            "behavior": BEHAVIORS[d.name][t],
            "development_hint": DEVELOPMENT_HINTS[d.name],
        })
    return result


def _build_section6_brain(assessment: AssessmentData) -> list[dict[str, Any]]:
    return [
        {
            "name": DOMAIN_DISPLAY_NAMES[d.name],
            "score": d.score,
            "color": AHIMS_COLORS[d.name],
            "brain_region": DOMAIN_BRAIN_REGIONS[d.name],
            "tier": _tier_label(d.score),
        }
        for d in assessment.domains
    ]


def _build_section7_architecture(assessment: AssessmentData) -> dict[str, Any]:
    b = _balance_score(assessment)
    flows = [
        {"from": "Attention", "to": "Learning", "strength": 0.8},
        {"from": "Memory", "to": "Learning", "strength": 0.7},
        {"from": "Processing", "to": "Problem Solving", "strength": 0.75},
        {"from": "Reasoning", "to": "Problem Solving", "strength": 0.85},
        {"from": "Learning", "to": "Daily Behaviour", "strength": 0.6},
        {"from": "Problem Solving", "to": "Daily Behaviour", "strength": 0.7},
        {"from": "Originality", "to": "Problem Solving", "strength": 0.5},
        {"from": "Emotional Intelligence", "to": "Daily Behaviour", "strength": 0.65},
        {"from": "Metacognition", "to": "Learning", "strength": 0.55},
        {"from": "Decision Integrity", "to": "Daily Behaviour", "strength": 0.6},
    ]
    return {
        "flows": flows,
        "balance_score": round(b, 1),
        "balance_level": "high" if b >= 80 else "moderate" if b >= 50 else "low",
    }


def _build_section8_functional(assessment: AssessmentData) -> list[dict[str, Any]]:
    scores = {DOMAIN_DISPLAY_NAMES[d.name]: d.score for d in assessment.domains}
    result = []
    for insight in FUNCTIONAL_INSIGHTS_DATA:
        contributing = []
        for dn in insight["domains"]:
            if dn in scores:
                contributing.append({"name": dn, "score": scores[dn], "color": AHIMS_COLORS.get(
                    next((k for k, v in DOMAIN_DISPLAY_NAMES.items() if v == dn), None), "#999"
                )})
        result.append({
            "title": insight["title"],
            "icon": insight["icon"],
            "description": insight["description"],
            "narrative": insight["narrative"],
            "domains": contributing,
        })
    return result


def _build_section9_interpersonal(assessment: AssessmentData) -> dict[str, Any]:
    scores = {DOMAIN_DISPLAY_NAMES[d.name]: d.score for d in assessment.domains}
    connections = []
    for conn in INTERPERSONAL_CONNECTIONS:
        domain_scores = []
        for dn in conn["domains"]:
            if dn in scores:
                domain_scores.append({"name": dn, "score": scores[dn], "color": AHIMS_COLORS.get(
                    next((k for k, v in DOMAIN_DISPLAY_NAMES.items() if v == dn), None), "#999"
                )})
        connections.append({
            "skill": conn["skill"],
            "description": conn["description"],
            "domains": domain_scores,
        })
    return {"connections": connections}


def _build_section10_persona(assessment: AssessmentData) -> dict[str, Any]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    primary = sorted_d[0]
    secondary = sorted_d[1] if len(sorted_d) > 1 else sorted_d[0]

    personas = {
        ("processing", "emotional_intelligence"): (
            "The Perceptive Processor",
            "Emotionally-attuned rapid cognition",
            "You navigate complex landscapes with equal fluency in analytical and social-cognitive information.",
            ["Speed + Empathy", "Dual Processing", "Social Precision"],
        ),
        ("attention", "memory"): (
            "The Analytical Observer",
            "Precision-driven pattern recognition",
            "You process information by carefully attending to detail and leveraging accumulated knowledge.",
            ["Deep Focus", "Pattern Recognition", "Thorough Analysis"],
        ),
        ("reasoning", "attention"): (
            "The Strategic Architect",
            "Systematic logical construction",
            "You construct logical frameworks and apply them with sustained concentration.",
            ["Logical Frameworks", "Strategic Focus", "Systematic Thinking"],
        ),
        ("emotional_intelligence", "metacognition"): (
            "The Reflective Navigator",
            "Emotionally-informed self-regulation",
            "You navigate social and cognitive landscapes with awareness of both external cues and internal states.",
            ["Emotional Insight", "Self-Awareness", "Adaptive Regulation"],
        ),
        ("originality", "reasoning"): (
            "The Innovative Analyst",
            "Creative-logical synthesis",
            "You generate novel solutions and evaluate them through logical frameworks.",
            ["Divergent Ideation", "Logical Evaluation", "Creative Synthesis"],
        ),
        ("processing", "attention"): (
            "The Rapid Integrator",
            "High-throughput focused processing",
            "You efficiently filter and process high volumes of information while maintaining accuracy.",
            ["Rapid Throughput", "Selective Focus", "Efficient Integration"],
        ),
        ("reasoning", "memory"): (
            "The Knowledge Architect",
            "Logic-grounded memory synthesis",
            "You apply stored knowledge structures to novel reasoning problems.",
            ["Knowledge Integration", "Logical Application", "Experiential Reasoning"],
        ),
        ("metacognition", "reasoning"): (
            "The Calibrated Thinker",
            "Self-aware analytical reasoning",
            "You monitor your own thinking while applying rigorous analytical frameworks.",
            ["Self-Monitoring", "Analytical Calibration", "Reflective Logic"],
        ),
    }

    key = (primary.name.value, secondary.name.value)
    reverse_key = (secondary.name.value, primary.name.value)

    if key in personas:
        name, descriptor, narrative, strengths = personas[key]
    elif reverse_key in personas:
        name, descriptor, narrative, strengths = personas[reverse_key]
    else:
        p = DOMAIN_DISPLAY_NAMES[primary.name]
        s = DOMAIN_DISPLAY_NAMES[secondary.name]
        name = f"The {p} Strategist"
        descriptor = f"{p}-centered cognitive architecture"
        narrative = f"Your cognitive identity is anchored in {p.lower()}, complemented by {s.lower()}."
        strengths = [p, s, "Strategic Thinking"]

    return {
        "name": name,
        "descriptor": descriptor,
        "narrative": narrative,
        "strengths": strengths,
        "working_style": f"You work best in environments that leverage your strength in {DOMAIN_DISPLAY_NAMES[primary.name].lower()} while providing structure for {DOMAIN_DISPLAY_NAMES[sorted_d[-1].name].lower()} development.",
    }


def _build_section11_development(assessment: AssessmentData) -> dict[str, Any]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score)
    priorities = []
    for i, d in enumerate(sorted_d[:3], 1):
        if d.score < 40:
            ease = "Hard"
            rationale = "Significant gap — requires sustained practice"
        elif d.score < 60:
            ease = "Moderate"
            rationale = "Moderate gap — steady practice yields gains"
        else:
            ease = "Easy"
            rationale = "Near threshold — targeted drills can close the gap"
        impact = "High" if i <= 2 else "Medium"
        impact_reason = "Core cognitive pillar" if d.name in (
            CognitiveDomainName.ATTENTION, CognitiveDomainName.REASONING,
            CognitiveDomainName.PROCESSING, CognitiveDomainName.MEMORY
        ) else "Supports broader cognitive integration"
        priorities.append({
            "rank": i,
            "name": DOMAIN_DISPLAY_NAMES[d.name],
            "score": d.score,
            "color": AHIMS_COLORS[d.name],
            "ease": ease,
            "impact": impact,
            "hint": DEVELOPMENT_HINTS[d.name],
            "rationale": rationale,
            "impact_reason": impact_reason,
        })

    top3 = [DOMAIN_DISPLAY_NAMES[d.name] for d in sorted_d[:3]]
    roadmap = [
        {"phase": "Week 1–2", "action": "Establish a baseline with " + top3[0].lower() + " exercises. " + DEVELOPMENT_HINTS[sorted_d[0].name].split('.')[0] + "."},
        {"phase": "Week 3–4", "action": "Increase " + top3[0].lower() + " intensity while introducing " + top3[1].lower() + " foundational work."},
        {"phase": "Month 2", "action": "Combine " + top3[0].lower() + " and " + top3[1].lower() + " in integrated sessions. " + DEVELOPMENT_HINTS[sorted_d[1].name].split('.')[0] + "."},
        {"phase": "Month 3+", "action": "Layer in " + top3[2].lower() + " development. " + DEVELOPMENT_HINTS[sorted_d[2].name].split('.')[0] + "."},
    ]

    return {"priorities": priorities, "roadmap": roadmap, "summary": "Your three focus areas are " + ", ".join(top3[:-1]) + ", and " + top3[-1] + ". Prioritise the first two for the highest impact on overall cognitive performance."}


def _build_section12_labs(assessment: AssessmentData) -> list[dict[str, Any]]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score)
    labs = {
        CognitiveDomainName.ATTENTION: ("Attentional Control Lab", "Sustained, selective, and divided attention exercises", "Enhances focus and distraction management", "Prefrontal Cortex"),
        CognitiveDomainName.MEMORY: ("Memory Architecture Lab", "Spaced repetition, chunking, and multi-modal consolidation", "Strengthens encoding and retrieval pathways", "Hippocampus"),
        CognitiveDomainName.PROCESSING: ("Processing Fluency Lab", "Speed and accuracy training with adaptive scaling", "Increases cognitive throughput", "Basal Ganglia"),
        CognitiveDomainName.REASONING: ("Reasoning Dynamics Lab", "Abstract and deductive reasoning exercises", "Sharpens analytical and logical thinking", "Dorsolateral PFC"),
        CognitiveDomainName.DECISION_INTEGRITY: ("Decision Architecture Lab", "Decision-making under varying cognitive loads", "Improves values-aligned judgment", "Anterior Cingulate"),
        CognitiveDomainName.EMOTIONAL_INTELLIGENCE: ("Emotional Perception Lab", "Emotional recognition and regulation practice", "Enhances social-cognitive awareness", "Insula & Amygdala"),
        CognitiveDomainName.ORIGINALITY: ("Divergent Thinking Lab", "Creative ideation with fluency and flexibility", "Expands creative problem-solving capacity", "Default Mode Network"),
        CognitiveDomainName.METACOGNITION: ("Metacognitive Awareness Lab", "Self-monitoring and strategy selection practice", "Strengthens self-regulated learning", "Frontopolar Cortex"),
    }

    result = []
    for i, d in enumerate(sorted_d[:3], 1):
        lab_name, lab_desc, benefit, brain_fn = labs[d.name]
        result.append({
            "rank": i,
            "domain_name": DOMAIN_DISPLAY_NAMES[d.name],
            "color": AHIMS_COLORS[d.name],
            "lab_name": lab_name,
            "lab_description": lab_desc,
            "expected_benefit": benefit,
            "brain_function": brain_fn,
        })
    return result


_BRAIN_IMAGE_MAP: dict[CognitiveDomainName, str] = {
    CognitiveDomainName.ATTENTION: "/static/assets/brain-attention.png",
    CognitiveDomainName.MEMORY: "/static/assets/brain-memory.png",
    CognitiveDomainName.PROCESSING: "/static/assets/brain-processing.png",
    CognitiveDomainName.REASONING: "/static/assets/brain-reasoning.png",
    CognitiveDomainName.DECISION_INTEGRITY: "/static/assets/brain-decision.png",
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: "/static/assets/brain-ei.png",
    CognitiveDomainName.ORIGINALITY: "/static/assets/brain-originality.png",
    CognitiveDomainName.METACOGNITION: "/static/assets/brain-metacognition.png",
}


def _build_glossary() -> list[dict[str, str]]:
    return [
        {
            "name": DOMAIN_DISPLAY_NAMES[d],
            "color": AHIMS_COLORS[d],
            "description": DOMAIN_SHORT_DESCRIPTIONS[d],
            "brain_region": DOMAIN_BRAIN_REGIONS[d],
            "brain_image": _BRAIN_IMAGE_MAP[d],
        }
        for d in CognitiveDomainName
    ]


# ---------------------------------------------------------------------------
# Main transformer
# ---------------------------------------------------------------------------

class CognitiveTransformer:
    def process(self, report: PsychometricReport) -> dict[str, Any]:
        a = report.assessment
        sorted_d = sorted(a.domains, key=lambda d: d.score, reverse=True)

        domain_data = [
            {
                "name": DOMAIN_DISPLAY_NAMES[d.name],
                "key": d.name.value,
                "score": d.score,
                "color": AHIMS_COLORS[d.name],
                "brain_region": DOMAIN_BRAIN_REGIONS[d.name],
                "narrative": TIER_NARRATIVES[_tier(d.score)],
                "behavior": BEHAVIORS[d.name][_tier(d.score)],
            }
            for d in a.domains
        ]

        return {
            "metadata": report.metadata,
            "participant_name": report.metadata.participant_name,
            "age": report.metadata.age,
            "gender": report.metadata.gender,
            "assessment_date": report.metadata.assessment_date.strftime("%B %d, %Y"),
            "assessment_id": report.metadata.assessment_id or "N/A",
            "company_logo": report.metadata.company_logo,
            "company_name": report.metadata.company_name,

            # Section 1 — Cover
            "overall_score": a.overall_score,
            "tier_label": _tier_label(a.overall_score),

            # Section 2 — Overview
            "section2": _build_section2_overview(a),

            # Section 3 — Executive
            "section3": _build_section3_executive(a),

            # Section 4 — Performance
            "section4": _build_section4_performance(a),

            # Section 5 — Domain Explorer
            "section5": _build_section5_explorer(a),

            # Section 6 — Brain
            "section6": _build_section6_brain(a),

            # Section 7 — Architecture
            "section7": _build_section7_architecture(a),

            # Section 8 — Functional
            "section8": _build_section8_functional(a),

            # Section 9 — Interpersonal
            "section9": _build_section9_interpersonal(a),

            # Section 10 — Persona
            "section10": _build_section10_persona(a),

            # Section 11 — Development
            "section11": _build_section11_development(a),

            # Section 12 — Labs
            "section12": _build_section12_labs(a),

            # Section 13 — Appendix
            "glossary": _build_glossary(),

            # JS data
            "domain_data_json": json.dumps(domain_data),
        }
