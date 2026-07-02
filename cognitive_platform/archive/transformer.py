"""Cognitive Intelligence Engine — 13-page report generation."""
from __future__ import annotations

import math
from typing import Any

from models.schema import (
    AssessmentData,
    CognitiveDomain,
    CognitiveDomainName,
    DevelopmentStage,
    DOMAIN_BRAIN_REGIONS,
    DOMAIN_DISPLAY_NAMES,
    DOMAIN_SEMANTIC_COLORS,
    DOMAIN_SHORT_DESCRIPTIONS,
    ExecutiveInsight,
    ExecutiveSummary,
    FunctionalBrainAssociation,
    HighlightBadge,
    InterpersonalInsight,
    Metadata,
    MethodologySection,
    PatternInsight,
    PerformanceOverview,
    PerformanceTier,
    ProcessedReport,
    PsychometricReport,
    RecommendedLab,
    CognitivePersona,
    DomainCard,
    DomainInterpretation,
)


# ---------------------------------------------------------------------------
# Tier system
# ---------------------------------------------------------------------------

_TIER_THRESHOLDS: list[tuple[float, PerformanceTier]] = [
    (85, PerformanceTier.DISTINGUISHED),
    (70, PerformanceTier.HIGH),
    (50, PerformanceTier.MODERATE),
    (0, PerformanceTier.DEVELOPING),
]

_TIER_LABELS: dict[PerformanceTier, str] = {
    PerformanceTier.DISTINGUISHED: "Distinguished",
    PerformanceTier.HIGH: "High",
    PerformanceTier.MODERATE: "Moderate",
    PerformanceTier.DEVELOPING: "Developing",
}

_TIER_NARRATIVES: dict[PerformanceTier, str] = {
    PerformanceTier.DISTINGUISHED: "Your results indicate a level of cognitive engagement that exceeds normative benchmarks. This pattern suggests robust neural efficiency in the assessed domain.",
    PerformanceTier.HIGH: "You demonstrate a strong capacity in this area, performing above the central tendency of the reference population. Your results suggest well-developed cognitive architecture.",
    PerformanceTier.MODERATE: "Your performance falls within the expected range for the general population. This indicates a stable cognitive foundation with opportunities for targeted development.",
    PerformanceTier.DEVELOPING: "Your results suggest this domain presents an area where additional engagement may yield meaningful improvement. This pattern reflects developmental opportunity.",
}

_MICRO_INSIGHTS: dict[CognitiveDomainName, dict[PerformanceTier, str]] = {
    CognitiveDomainName.ATTENTION: {
        PerformanceTier.DISTINGUISHED: "Sustained focus with minimal attentional drift across extended tasks.",
        PerformanceTier.HIGH: "Reliable attentional control with effective distractor filtering.",
        PerformanceTier.MODERATE: "Typical attentional span with intermittent variability.",
        PerformanceTier.DEVELOPING: "Opportunity to strengthen sustained attention patterns.",
    },
    CognitiveDomainName.MEMORY: {
        PerformanceTier.DISTINGUISHED: "Exceptional encoding and retrieval efficiency across modalities.",
        PerformanceTier.HIGH: "Strong working and episodic memory capacity.",
        PerformanceTier.MODERATE: "Standard memory performance with consistent baseline.",
        PerformanceTier.DEVELOPING: "Memory consolidation pathways may benefit from reinforcement.",
    },
    CognitiveDomainName.PROCESSING: {
        PerformanceTier.DISTINGUISHED: "Rapid information throughput with sustained accuracy.",
        PerformanceTier.HIGH: "Efficient neural transmission and task switching.",
        PerformanceTier.MODERATE: "Standard processing throughput under normal conditions.",
        PerformanceTier.DEVELOPING: "Processing speed shows room for fluency development.",
    },
    CognitiveDomainName.REASONING: {
        PerformanceTier.DISTINGUISHED: "Sophisticated abstract and deductive reasoning capacity.",
        PerformanceTier.HIGH: "Effective logical reasoning and pattern recognition.",
        PerformanceTier.MODERATE: "Competent reasoning within familiar problem structures.",
        PerformanceTier.DEVELOPING: "Abstract reasoning capacity is emerging.",
    },
    CognitiveDomainName.DECISION_INTEGRITY: {
        PerformanceTier.DISTINGUISHED: "Consistent values-aligned decision architecture under pressure.",
        PerformanceTier.HIGH: "Sound judgment under moderate cognitive load.",
        PerformanceTier.MODERATE: "Standard decision-making with context sensitivity.",
        PerformanceTier.DEVELOPING: "Decision processes may benefit from structured reflection.",
    },
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: {
        PerformanceTier.DISTINGUISHED: "Refined emotional perception, interpretation, and regulation.",
        PerformanceTier.HIGH: "Strong empathic accuracy and emotional awareness.",
        PerformanceTier.MODERATE: "Standard emotional recognition and response patterns.",
        PerformanceTier.DEVELOPING: "Emotional processing pathways are open to development.",
    },
    CognitiveDomainName.ORIGINALITY: {
        PerformanceTier.DISTINGUISHED: "Novel ideation with divergent fluency and flexibility.",
        PerformanceTier.HIGH: "Creative flexibility across problem domains.",
        PerformanceTier.MODERATE: "Conventional thinking with occasional novel approaches.",
        PerformanceTier.DEVELOPING: "Divergent thinking capacity is emerging.",
    },
    CognitiveDomainName.METACOGNITION: {
        PerformanceTier.DISTINGUISHED: "Highly accurate self-monitoring and strategy calibration.",
        PerformanceTier.HIGH: "Effective self-regulation and adaptive strategy selection.",
        PerformanceTier.MODERATE: "Standard self-awareness with typical calibration.",
        PerformanceTier.DEVELOPING: "Metacognitive monitoring is developing.",
    },
}

_FUNCTIONAL_BEHAVIORS: dict[CognitiveDomainName, dict[PerformanceTier, str]] = {
    CognitiveDomainName.ATTENTION: {
        PerformanceTier.DISTINGUISHED: "You maintain selective focus across extended tasks with minimal decoy interference.",
        PerformanceTier.HIGH: "You effectively filter distractors in moderately complex environments.",
        PerformanceTier.MODERATE: "You sustain attention adequately for standard-duration tasks.",
        PerformanceTier.DEVELOPING: "You benefit from structured attentional cueing in complex settings.",
    },
    CognitiveDomainName.MEMORY: {
        PerformanceTier.DISTINGUISHED: "You consolidate and retrieve information with high fidelity across delays.",
        PerformanceTier.HIGH: "You retain and recall structured information reliably.",
        PerformanceTier.MODERATE: "You encode and retrieve information at expected rates.",
        PerformanceTier.DEVELOPING: "You benefit from repetition and multi-modal encoding.",
    },
    CognitiveDomainName.PROCESSING: {
        PerformanceTier.DISTINGUISHED: "You execute rapid cognitive operations without accuracy trade-offs.",
        PerformanceTier.HIGH: "You complete sequential and parallel tasks efficiently.",
        PerformanceTier.MODERATE: "You process information at a steady, functional pace.",
        PerformanceTier.DEVELOPING: "You show slower throughput that may improve with practice.",
    },
    CognitiveDomainName.REASONING: {
        PerformanceTier.DISTINGUISHED: "You apply abstract rules flexibly across novel problem spaces.",
        PerformanceTier.HIGH: "You solve deductive and inductive problems consistently.",
        PerformanceTier.MODERATE: "You reason effectively within familiar logical frameworks.",
        PerformanceTier.DEVELOPING: "You are developing capacity for abstract reasoning.",
    },
    CognitiveDomainName.DECISION_INTEGRITY: {
        PerformanceTier.DISTINGUISHED: "Your decisions reflect strong consistency with internalized values.",
        PerformanceTier.HIGH: "You maintain decision coherence across varying cognitive loads.",
        PerformanceTier.MODERATE: "You make sound decisions under typical conditions.",
        PerformanceTier.DEVELOPING: "You benefit from structured decision frameworks.",
    },
    CognitiveDomainName.EMOTIONAL_INTELLIGENCE: {
        PerformanceTier.DISTINGUISHED: "You perceive, interpret, and regulate emotional information with nuance.",
        PerformanceTier.HIGH: "You demonstrate strong awareness of emotional cues.",
        PerformanceTier.MODERATE: "You respond to emotional information at expected levels.",
        PerformanceTier.DEVELOPING: "You are building capacity for emotional perception.",
    },
    CognitiveDomainName.ORIGINALITY: {
        PerformanceTier.DISTINGUISHED: "You generate diverse, original solutions with fluency.",
        PerformanceTier.HIGH: "You apply creative thinking across unfamiliar contexts.",
        PerformanceTier.MODERATE: "You produce conventional solutions with occasional novelty.",
        PerformanceTier.DEVELOPING: "You are developing divergent ideation capacity.",
    },
    CognitiveDomainName.METACOGNITION: {
        PerformanceTier.DISTINGUISHED: "You accurately monitor your own cognitive processes and adjust proactively.",
        PerformanceTier.HIGH: "You self-regulate effectively and select appropriate strategies.",
        PerformanceTier.MODERATE: "You demonstrate standard self-awareness of cognitive strengths.",
        PerformanceTier.DEVELOPING: "You are developing awareness of your own thinking.",
    },
}


def _score_tier(score: float) -> PerformanceTier:
    for threshold, tier in _TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    return PerformanceTier.DEVELOPING


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def _build_domain_interpretation(domain: CognitiveDomain) -> DomainInterpretation:
    tier = _score_tier(domain.score)
    return DomainInterpretation(
        domain=domain.name,
        display_name=DOMAIN_DISPLAY_NAMES[domain.name],
        score=domain.score,
        tier=tier,
        color=DOMAIN_SEMANTIC_COLORS[domain.name],
        brain_region=DOMAIN_BRAIN_REGIONS[domain.name],
        narrative=_TIER_NARRATIVES[tier],
        micro_insight=_MICRO_INSIGHTS[domain.name][tier],
        functional_behavior=_FUNCTIONAL_BEHAVIORS[domain.name][tier],
    )


# --- Page 1: Cover -------------------------------------------------------

def _build_cover_tagline(assessment: AssessmentData) -> str:
    score = assessment.overall_score
    tier = _score_tier(score)
    if score >= 80:
        return "A cognitive profile of remarkable breadth and depth."
    elif score >= 65:
        return "A balanced cognitive architecture with distinctive strengths."
    else:
        return "A differentiated cognitive profile with clear developmental pathways."


# --- Page 2: Participant Overview -----------------------------------------

def _build_highlight_badges(assessment: AssessmentData) -> list[HighlightBadge]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    top = sorted_d[0]
    bottom = sorted_d[-1]
    mean_score = sum(d.score for d in assessment.domains) / len(assessment.domains)

    badges = [
        HighlightBadge(
            label="Strongest Domain",
            value=DOMAIN_DISPLAY_NAMES[top.name],
            color=DOMAIN_SEMANTIC_COLORS[top.name],
        ),
        HighlightBadge(
            label="Top Score",
            value=f"{top.score:.0f}%",
            color="#2D3436",
        ),
        HighlightBadge(
            label="Development Focus",
            value=DOMAIN_DISPLAY_NAMES[bottom.name],
            color=DOMAIN_SEMANTIC_COLORS[bottom.name],
        ),
    ]

    scores = [d.score for d in assessment.domains]
    spread = max(scores) - min(scores)
    if spread <= 15:
        badges.append(HighlightBadge(label="Profile Balance", value="Highly Balanced", color="#00B894"))
    elif spread <= 30:
        badges.append(HighlightBadge(label="Profile Balance", value="Moderately Balanced", color="#FDCB6E"))
    else:
        badges.append(HighlightBadge(label="Profile Balance", value="Differentiated", color="#E17055"))

    return badges


def _build_overview_summary(assessment: AssessmentData) -> str:
    tier = _score_tier(assessment.overall_score)
    mean_score = sum(d.score for d in assessment.domains) / len(assessment.domains)
    scores = [d.score for d in assessment.domains]
    spread = max(scores) - min(scores)

    parts = [
        f"Your overall cognitive performance score of {assessment.overall_score:.0f}% places you in the {_TIER_LABELS[tier].lower()} tier.",
    ]
    if spread <= 15:
        parts.append("Your profile exhibits a high degree of cognitive balance across all assessed domains, suggesting well-coordinated neural networks.")
    elif spread <= 30:
        parts.append("Your profile shows moderate variability across cognitive domains, which is typical of differentiated cognitive development.")
    else:
        parts.append("Your profile shows significant variability across domains, indicating a differentiated cognitive architecture with distinct strengths.")

    return " ".join(parts)


# --- Page 3: Executive Summary -------------------------------------------

def _build_executive_summary(assessment: AssessmentData) -> ExecutiveSummary:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    tier = _score_tier(assessment.overall_score)

    top_three = sorted_d[:3]
    bottom_three = sorted_d[-3:]

    insights = [
        ExecutiveInsight(
            title="Primary Strength",
            body=(
                f"Your highest-performing domain is {DOMAIN_DISPLAY_NAMES[top_three[0].name]} "
                f"at {top_three[0].score:.0f}%, placing it in the "
                f"{_TIER_LABELS[_score_tier(top_three[0].score)].lower()} tier. "
                f"This suggests particularly efficient neural architecture in this cognitive system."
            ),
        ),
        ExecutiveInsight(
            title="Cognitive Balance",
            body=(
                f"Across all eight domains, your scores range from "
                f"{bottom_three[-1].score:.0f}% to {top_three[0].score:.0f}%, "
                f"a spread of {top_three[0].score - bottom_three[-1].score:.0f} percentage points. "
                f"{'This indicates a balanced cognitive profile.' if (top_three[0].score - bottom_three[-1].score) <= 20 else 'This indicates a differentiated cognitive architecture.'}"
            ),
        ),
        ExecutiveInsight(
            title="Development Opportunity",
            body=(
                f"Your lowest-scoring domain is {DOMAIN_DISPLAY_NAMES[bottom_three[-1].name]} "
                f"at {bottom_three[-1].score:.0f}%. This area presents the most opportunity "
                f"for targeted cognitive development through structured engagement."
            ),
        ),
    ]

    narrative = (
        f"Your cognitive profile reveals a {_TIER_LABELS[tier].lower()} overall performance "
        f"pattern across eight assessed domains. The following insights synthesize the most "
        f"significant findings from your assessment data."
    )

    closing = (
        "These findings provide a foundation for understanding your cognitive architecture "
        "and identifying pathways for continued development."
    )

    return ExecutiveSummary(
        narrative=narrative,
        insights=insights,
        closing_takeaway=closing,
    )


# --- Page 4: Performance Dashboard ---------------------------------------

def _build_performance_overview(assessment: AssessmentData) -> PerformanceOverview:
    tier = _score_tier(assessment.overall_score)
    interpretations = [_build_domain_interpretation(d) for d in assessment.domains]

    summary = (
        f"Your cognitive performance across eight domains reveals a profile "
        f"that places you in the {_TIER_LABELS[tier].lower()} tier overall. "
        f"The following visualization maps your domain scores into a cognitive "
        f"constellation, where each node represents a functional cognitive system."
    )

    callout = (
        "The relative positions and intensities of each node reflect your "
        "performance pattern. Nodes closer to the outer ring indicate higher "
        "performance, while connections between nodes suggest cognitive "
        "integration across domains."
    )

    return PerformanceOverview(
        summary_statement=summary,
        overall_score=assessment.overall_score,
        overall_tier=tier,
        domain_interpretations=interpretations,
        constellation_data=_build_constellation_data(assessment),
        interpretation_callout=callout,
    )


# --- Page 5: Brain Associations ------------------------------------------

def _build_brain_associations(assessment: AssessmentData) -> list[FunctionalBrainAssociation]:
    associations = []
    for d in assessment.domains:
        tier = _score_tier(d.score)
        associations.append(
            FunctionalBrainAssociation(
                domain=d.name,
                display_name=DOMAIN_DISPLAY_NAMES[d.name],
                color=DOMAIN_SEMANTIC_COLORS[d.name],
                brain_region=DOMAIN_BRAIN_REGIONS[d.name],
                functional_role=DOMAIN_SHORT_DESCRIPTIONS[d.name],
                association_note=_FUNCTIONAL_BEHAVIORS[d.name][tier],
            )
        )
    return associations


# --- Page 6: Domain Matrix ------------------------------------------------

def _build_domain_cards(assessment: AssessmentData) -> list[DomainCard]:
    cards = []
    for d in assessment.domains:
        tier = _score_tier(d.score)
        cards.append(
            DomainCard(
                domain=d.name,
                display_name=DOMAIN_DISPLAY_NAMES[d.name],
                score=d.score,
                tier=tier,
                color=DOMAIN_SEMANTIC_COLORS[d.name],
                short_description=DOMAIN_SHORT_DESCRIPTIONS[d.name],
                interpretation=_MICRO_INSIGHTS[d.name][tier],
            )
        )
    return sorted(cards, key=lambda c: c.score, reverse=True)


# --- Page 7: Pattern Analysis --------------------------------------------

def _build_pattern_insights(assessment: AssessmentData) -> tuple[list[PatternInsight], str]:
    scores = {d.name: d.score for d in assessment.domains}
    mean_val = sum(scores.values()) / len(scores)
    high = [k for k, v in scores.items() if v >= mean_val + 10]
    low = [k for k, v in scores.items() if v <= mean_val - 10]
    balanced = [k for k, v in scores.items() if mean_val - 10 < v < mean_val + 10]

    insights: list[PatternInsight] = []

    if high:
        insights.append(
            PatternInsight(
                title="Elevated Cognitive Cluster",
                description=(
                    f"Your scores in {', '.join(DOMAIN_DISPLAY_NAMES[h] for h in high[:3])} "
                    f"exceed your personal mean by more than 10 percentage points. "
                    f"This pattern suggests a cognitive architecture with pronounced "
                    f"strengths in these interconnected domains."
                ),
                domains_involved=[DOMAIN_DISPLAY_NAMES[h] for h in high[:3]],
                significance="These domains form the core of your cognitive identity and likely drive your strongest performance outcomes.",
            )
        )

    if low:
        insights.append(
            PatternInsight(
                title="Development Opportunity Cluster",
                description=(
                    f"Your scores in {', '.join(DOMAIN_DISPLAY_NAMES[l] for l in low[:3])} "
                    f"fall below your personal mean by more than 10 percentage points. "
                    f"These domains represent areas where targeted engagement may "
                    f"yield the most significant developmental returns."
                ),
                domains_involved=[DOMAIN_DISPLAY_NAMES[l] for l in low[:3]],
                significance="Investment in these areas may have a multiplicative effect on your overall cognitive performance.",
            )
        )

    if len(balanced) >= 3:
        insights.append(
            PatternInsight(
                title="Stable Cognitive Foundation",
                description=(
                    f"Your scores in {', '.join(DOMAIN_DISPLAY_NAMES[b] for b in balanced[:4])} "
                    f"cluster within 10 percentage points of your mean. This stable "
                    f"foundation provides reliable cognitive resources that support "
                    f"adaptive functioning across varied contexts."
                ),
                domains_involved=[DOMAIN_DISPLAY_NAMES[b] for b in balanced[:4]],
                significance="This stable baseline suggests consistent cognitive reliability in everyday tasks.",
            )
        )

    # Cognitive integration pattern
    reasoning_score = scores.get(CognitiveDomainName.REASONING, 0)
    metacog_score = scores.get(CognitiveDomainName.METACOGNITION, 0)
    if reasoning_score >= 70 and metacog_score >= 70:
        insights.append(
            PatternInsight(
                title="Analytical Self-Awareness Pattern",
                description=(
                    "Your reasoning and metacognition scores both exceed 70%, "
                    "indicating a cognitive pattern where analytical capacity is "
                    "complemented by strong self-monitoring. This integration "
                    "suggests effective self-regulated learning."
                ),
                domains_involved=["Reasoning", "Metacognition"],
                significance="This pattern is associated with adaptive expertise and efficient strategy selection.",
            )
        )

    ei_score = scores.get(CognitiveDomainName.EMOTIONAL_INTELLIGENCE, 0)
    attention_score = scores.get(CognitiveDomainName.ATTENTION, 0)
    if ei_score >= 75 and attention_score >= 75:
        insights.append(
            PatternInsight(
                title="Perceptive Attunement Pattern",
                description=(
                    "Your emotional intelligence and attention scores both demonstrate "
                    "strong performance, suggesting a cognitive pattern where emotional "
                    "perception is supported by sustained attentional focus."
                ),
                domains_involved=["Emotional Intelligence", "Attention"],
                significance="This integration supports nuanced social-cognitive processing.",
            )
        )

    summary = (
        f"Your cognitive profile reveals {'multiple meaningful patterns' if len(insights) > 1 else 'a distinct pattern'} "
        f"across the assessed domains. These patterns emerge from the relationships "
        f"between your domain scores and reflect the integrated nature of your "
        f"cognitive architecture."
    )

    return insights, summary


# --- Page 8: Persona ------------------------------------------------------

def _build_persona(assessment: AssessmentData) -> CognitivePersona:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)
    primary = sorted_d[0]
    secondary = sorted_d[1] if len(sorted_d) > 1 else sorted_d[0]

    persona_map: dict[tuple[str, str], tuple[str, str, str, list[str], str]] = {
        ("processing", "emotional_intelligence"): (
            "The Perceptive Processor",
            "Emotionally-attuned rapid cognition",
            "Your cognitive identity is defined by the intersection of rapid information processing and refined emotional perception. You process both analytical and social-cognitive information with speed and nuance, suggesting highly integrated neural systems. This combination allows you to navigate complex interpersonal and analytical landscapes with equal fluency.",
            ["Rapid Processing", "Emotional Attunement", "Social Precision", "Analytical Speed"],
            "perceptive-processor",
        ),
        ("attention", "memory"): (
            "The Analytical Observer",
            "Precision-driven pattern recognition",
            "Your cognitive architecture is built around sustained attentional control and robust memory encoding. You process information by carefully attending to detail and leveraging accumulated knowledge structures, building comprehensive mental models of complex situations.",
            ["Sustained Focus", "Deep Encoding", "Pattern Memory", "Analytical Thoroughness"],
            "analytical-observer",
        ),
        ("reasoning", "attention"): (
            "The Strategic Architect",
            "Systematic logical construction",
            "Your cognitive strengths center on abstract reasoning and focused attention. You construct logical frameworks and apply them with sustained concentration, enabling complex problem decomposition and systematic solution building.",
            ["Logical Frameworks", "Sustained Analysis", "Systematic Thinking", "Strategic Focus"],
            "strategic-architect",
        ),
        ("emotional_intelligence", "metacognition"): (
            "The Reflective Navigator",
            "Emotionally-informed self-regulation",
            "Your cognitive profile combines emotional perception with strong self-monitoring capacity. You navigate social and cognitive landscapes with awareness of both external emotional cues and your own internal processing states.",
            ["Emotional Insight", "Self-Awareness", "Reflective Judgment", "Adaptive Regulation"],
            "reflective-navigator",
        ),
        ("originality", "reasoning"): (
            "The Innovative Analyst",
            "Creative-logical synthesis",
            "Your cognitive architecture uniquely combines divergent ideation with analytical reasoning. You generate novel solutions and evaluate them through logical frameworks, producing creative outcomes that are both original and structurally sound.",
            ["Divergent Ideation", "Logical Evaluation", "Creative Synthesis", "Innovative Problem-Solving"],
            "innovative-analyst",
        ),
        ("processing", "attention"): (
            "The Rapid Integrator",
            "High-throughput focused processing",
            "Your cognitive profile excels in rapid information processing combined with selective attention. You efficiently filter and process high volumes of information while maintaining accuracy, suggesting strong neural transmission efficiency.",
            ["Rapid Throughput", "Selective Focus", "Efficient Integration", "Dynamic Processing"],
            "rapid-integrator",
        ),
        ("processing", "memory"): (
            "The Fluent Encoder",
            "Rapid encoding and retrieval",
            "Your cognitive strengths center on processing speed and memory consolidation. You encode new information rapidly and retrieve stored knowledge efficiently, suggesting well-optimized neural pathways.",
            ["Fast Encoding", "Reliable Retrieval", "Knowledge Fluency", "Memory Speed"],
            "fluent-encoder",
        ),
        ("attention", "reasoning"): (
            "The Focused Analyst",
            "Sustained logical concentration",
            "Your cognitive profile combines sustained attentional control with strong analytical reasoning. You maintain focus on complex logical problems over extended periods, building thorough solutions.",
            ["Sustained Concentration", "Logical Rigor", "Deep Analysis", "Focused Problem-Solving"],
            "focused-analyst",
        ),
        ("reasoning", "memory"): (
            "The Knowledge Architect",
            "Logic-grounded memory synthesis",
            "Your cognitive identity is built on the intersection of logical reasoning and robust memory systems. You apply stored knowledge structures to novel reasoning problems, constructing solutions grounded in experience.",
            ["Knowledge Integration", "Logical Application", "Experiential Reasoning", "Memory-Guided Analysis"],
            "knowledge-architect",
        ),
        ("metacognition", "reasoning"): (
            "The Calibrated Thinker",
            "Self-aware analytical reasoning",
            "Your cognitive strengths lie in the integration of metacognitive awareness and logical reasoning. You monitor your own thinking while applying rigorous analytical frameworks, producing well-calibrated reasoning.",
            ["Self-Monitoring", "Analytical Calibration", "Reflective Logic", "Adaptive Thinking"],
            "calibrated-thinker",
        ),
        ("originality", "attention"): (
            "The Focused Visionary",
            "Sustained creative concentration",
            "Your cognitive profile combines creative ideation with the sustained attention needed to develop novel ideas to completion. You generate original concepts and maintain the focus to refine them.",
            ["Creative Focus", "Sustained Ideation", "Novel Development", "Visionary Concentration"],
            "focused-visionary",
        ),
        ("emotional_intelligence", "attention"): (
            "The Attuned Observer",
            "Emotionally perceptive sustained focus",
            "Your cognitive architecture blends emotional perception with sustained attentional awareness. You perceive both emotional nuances and analytical details with equal clarity.",
            ["Emotional Perception", "Sustained Attunement", "Dual Awareness", "Perceptive Focus"],
            "attuned-observer",
        ),
        ("originality", "emotional_intelligence"): (
            "The Empathic Innovator",
            "Emotionally-grounded creative thinking",
            "Your cognitive identity combines creative ideation with deep emotional awareness. You generate novel solutions that account for human emotional experience, producing innovations with empathic resonance.",
            ["Empathic Creativity", "Human-Centered Innovation", "Emotional Originality", "Compassionate Ideation"],
            "empathic-innovator",
        ),
        ("originality", "processing"): (
            "The Creative Accelerator",
            "Rapid divergent ideation",
            "Your cognitive profile merges creative fluency with processing speed. You generate diverse ideas rapidly, suggesting highly efficient creative throughput and the ability to explore wide solution spaces quickly.",
            ["Rapid Ideation", "Creative Fluency", "Fast Divergence", "Speed-Driven Innovation"],
            "creative-accelerator",
        ),
        ("metacognition", "emotional_intelligence"): (
            "The Insightful Regulator",
            "Self-and-other aware cognition",
            "Your cognitive architecture integrates metacognitive awareness with emotional intelligence. You monitor your own cognitive and emotional states while remaining attuned to the emotional experiences of others.",
            ["Dual Awareness", "Emotional Self-Regulation", "Insightful Monitoring", "Relational Intelligence"],
            "insightful-regulator",
        ),
    }

    key = (primary.name.value, secondary.name.value)
    reverse_key = (secondary.name.value, primary.name.value)

    if key in persona_map:
        title, descriptor, narrative, tags, motif = persona_map[key]
    elif reverse_key in persona_map:
        title, descriptor, narrative, tags, motif = persona_map[reverse_key]
    else:
        p_name = DOMAIN_DISPLAY_NAMES[primary.name]
        s_name = DOMAIN_DISPLAY_NAMES[secondary.name]
        title = f"The {p_name} Strategist"
        descriptor = f"{p_name}-centered cognitive architecture"
        narrative = (
            f"Your cognitive identity is anchored in {p_name.lower()}, "
            f"complemented by {s_name.lower()}. This combination shapes how "
            f"you perceive, process, and respond to cognitive challenges, with "
            f"particular efficiency in tasks requiring both capacities."
        )
        tags = [p_name, s_name, "Strategic Thinking", "Targeted Cognition"]
        motif = "default-strategist"

    return CognitivePersona(
        title=title,
        descriptor=descriptor,
        narrative=narrative,
        trait_tags=tags,
        persona_motif=motif,
    )


# --- Page 9: Interpersonal Insights --------------------------------------

def _build_interpersonal_insights(assessment: AssessmentData) -> list[InterpersonalInsight]:
    scores = {d.name: d.score for d in assessment.domains}
    ei = scores.get(CognitiveDomainName.EMOTIONAL_INTELLIGENCE, 50)
    attention = scores.get(CognitiveDomainName.ATTENTION, 50)
    reasoning = scores.get(CognitiveDomainName.REASONING, 50)
    processing = scores.get(CognitiveDomainName.PROCESSING, 50)
    metacog = scores.get(CognitiveDomainName.METACOGNITION, 50)

    insights: list[InterpersonalInsight] = []

    # Collaboration style
    if ei >= 75:
        insights.append(
            InterpersonalInsight(
                title="Collaborative Strength",
                category="Collaboration",
                description="Your strong emotional intelligence suggests you bring empathic awareness and social perceptiveness to collaborative settings. You naturally attune to group dynamics and adjust your approach based on interpersonal cues.",
                communication_cues=["Active listening", "Empathic responding", "Conflict sensitivity"],
            )
        )
    else:
        insights.append(
            InterpersonalInsight(
                title="Analytical Collaboration",
                category="Collaboration",
                description="Your cognitive profile suggests you contribute analytical rigor and structured thinking to group work. You bring clarity and logical coherence to collaborative problem-solving.",
                communication_cues=["Structured input", "Logical framing", "Evidence-based reasoning"],
            )
        )

    # Communication style
    if processing >= 75 and attention >= 75:
        insights.append(
            InterpersonalInsight(
                title="Rapid-Fire Communication",
                category="Communication",
                description="Your combination of processing speed and attention suggests you process and respond to information quickly in conversations. You may prefer fast-paced exchanges and rapid idea iteration.",
                communication_cues=["Quick synthesis", "Concise expression", "Rapid feedback loops"],
            )
        )
    elif reasoning >= 75:
        insights.append(
            InterpersonalInsight(
                title="Deliberate Communication",
                category="Communication",
                description="Your reasoning strength suggests you prefer thoughtful, well-constructed communication. You take time to process information thoroughly before responding, contributing depth to discussions.",
                communication_cues=["Measured responses", "Thorough analysis", "Logical structure"],
            )
        )
    else:
        insights.append(
            InterpersonalInsight(
                title="Balanced Communication",
                category="Communication",
                description="Your cognitive profile suggests a balanced communication style that adapts to context. You can engage in both rapid exchanges and deeper, more reflective discussions as needed.",
                communication_cues=["Contextual adaptation", "Balanced pacing", "Flexible engagement"],
            )
        )

    # Decision-making in groups
    if scores.get(CognitiveDomainName.DECISION_INTEGRITY, 50) >= 70:
        insights.append(
            InterpersonalInsight(
                title="Values-Driven Decision Making",
                category="Decision Making",
                description="Your decision integrity score suggests you bring consistent, values-aligned judgment to group decisions. Others can rely on your decision-making under pressure.",
                communication_cues=["Transparent reasoning", "Consistent values", "Reliable judgment"],
            )
        )

    # Learning dynamics
    if metacog >= 70:
        insights.append(
            InterpersonalInsight(
                title="Self-Aware Learning Partner",
                category="Learning",
                description="Your metacognitive awareness means you understand your own learning processes well. This allows you to communicate your needs clearly and adapt to different collaborative learning contexts.",
                communication_cues=["Self-assessment", "Transparent learning needs", "Adaptive strategies"],
            )
        )

    return insights


# --- Page 10: Development Strategy ---------------------------------------

def _build_development_stages(assessment: AssessmentData) -> list[DevelopmentStage]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score)

    stages = [
        DevelopmentStage(
            stage="Foundation",
            focus_area=DOMAIN_DISPLAY_NAMES[sorted_d[0].name],
            description=(
                f"Begin with targeted engagement in {DOMAIN_DISPLAY_NAMES[sorted_d[0].name].lower()}, "
                f"your current lowest-scoring domain. Structured exercises in this area "
                f"can establish a stronger cognitive baseline."
            ),
            priority="High",
            actions=[
                f"Engage with {DOMAIN_DISPLAY_NAMES[sorted_d[0].name]}-focused cognitive exercises",
                "Establish consistent practice patterns",
                "Track progress through periodic reassessment",
            ],
        ),
        DevelopmentStage(
            stage="Integration",
            focus_area="Cross-Domain Connections",
            description=(
                f"Once {DOMAIN_DISPLAY_NAMES[sorted_d[0].name].lower()} shows improvement, "
                f"focus on integrating this development with your existing strengths "
                f"in {DOMAIN_DISPLAY_NAMES[sorted_d[-1].name].lower()} and "
                f"{DOMAIN_DISPLAY_NAMES[sorted_d[-2].name].lower()}."
            ),
            priority="Medium",
            actions=[
                "Practice tasks requiring multiple cognitive domains simultaneously",
                "Build bridges between your strengths and development areas",
                "Seek complex, multi-dimensional challenges",
            ],
        ),
        DevelopmentStage(
            stage="Refinement",
            focus_area="Advanced Application",
            description=(
                f"With a stronger foundation, shift focus to advanced application "
                f"of your cognitive strengths in real-world contexts that demand "
                f"integrated performance across domains."
            ),
            priority="Standard",
            actions=[
                "Apply cognitive gains to professional and personal contexts",
                "Engage in complex, open-ended problem solving",
                "Continue periodic assessment to track long-term development",
            ],
        ),
    ]

    return stages


# --- Page 11: Recommended Labs -------------------------------------------

def _build_recommended_labs(assessment: AssessmentData) -> list[RecommendedLab]:
    sorted_d = sorted(assessment.domains, key=lambda d: d.score)

    labs: dict[CognitiveDomainName, tuple[str, str, str]] = {
        CognitiveDomainName.ATTENTION: (
            "Attentional Control Lab",
            "Structured exercises targeting sustained, selective, and divided attention through progressive cognitive challenges.",
            "Attention forms the gateway for all cognitive processing. Strengthening attentional control enhances performance across every other domain.",
        ),
        CognitiveDomainName.MEMORY: (
            "Memory Architecture Lab",
            "Encoding and retrieval practice using spaced repetition, chunking strategies, and multi-modal memory consolidation.",
            "Memory provides the knowledge foundation for reasoning and decision-making. Enhanced memory systems support more efficient cognitive operation.",
        ),
        CognitiveDomainName.PROCESSING: (
            "Processing Fluency Lab",
            "Speed and accuracy training through timed cognitive tasks with adaptive difficulty scaling.",
            "Processing speed determines how quickly you can execute cognitive operations. Improving fluency enhances overall cognitive throughput.",
        ),
        CognitiveDomainName.REASONING: (
            "Reasoning Dynamics Lab",
            "Abstract and deductive reasoning exercises using novel problem structures and logical sequencing challenges.",
            "Reasoning is the core analytical engine of cognition. Strengthening reasoning capacity improves problem-solving across all domains.",
        ),
        CognitiveDomainName.DECISION_INTEGRITY: (
            "Decision Architecture Lab",
            "Structured decision-making practice under varying cognitive loads with feedback on consistency and alignment.",
            "Decision integrity ensures your cognitive strengths translate into consistent, values-aligned choices under real-world pressure.",
        ),
        CognitiveDomainName.EMOTIONAL_INTELLIGENCE: (
            "Emotional Perception Lab",
            "Emotional recognition and regulation exercises using scenario-based practice and empathic accuracy training.",
            "Emotional intelligence bridges cognitive processing with social-cognitive effectiveness, enhancing collaboration and interpersonal outcomes.",
        ),
        CognitiveDomainName.ORIGINALITY: (
            "Divergent Thinking Lab",
            "Creative ideation exercises emphasizing fluency, flexibility, and originality through constrained problem solving.",
            "Originality drives innovation and adaptive problem-solving. Developing creative capacity expands your cognitive repertoire.",
        ),
        CognitiveDomainName.METACOGNITION: (
            "Metacognitive Awareness Lab",
            "Self-monitoring and strategy selection practice with calibration feedback and reflective exercises.",
            "Metacognition is the multiplier that enhances all other cognitive domains through better self-regulation and strategy selection.",
        ),
    }

    recommended: list[RecommendedLab] = []
    for rank, domain in enumerate(sorted_d[:3], start=1):
        tier = _score_tier(domain.score)
        lab_name, lab_desc, rationale = labs[domain.name]
        recommended.append(
            RecommendedLab(
                rank=rank,
                domain=domain.name,
                display_name=DOMAIN_DISPLAY_NAMES[domain.name],
                color=DOMAIN_SEMANTIC_COLORS[domain.name],
                title=f"Develop {DOMAIN_DISPLAY_NAMES[domain.name]} Capacity",
                description=(
                    f"Your {DOMAIN_DISPLAY_NAMES[domain.name].lower()} score of "
                    f"{domain.score:.0f}% places this domain in the "
                    f"{_TIER_LABELS[tier].lower()} tier. Targeted engagement "
                    f"with structured cognitive exercises may yield meaningful development."
                ),
                lab_name=lab_name,
                lab_description=lab_desc,
                rationale=rationale,
            )
        )
    return recommended


# --- Page 12: Methodology -------------------------------------------------

def _build_methodology() -> list[MethodologySection]:
    return [
        MethodologySection(
            title="Assessment Framework",
            content="This cognitive assessment evaluates eight domains of cognitive function using standardized psychometric instruments. Each domain is assessed through multiple subtests designed to measure specific cognitive operations. Scores are computed against age-normed reference data and expressed as percentiles relative to the general population.",
        ),
        MethodologySection(
            title="Scoring Model",
            content="Domain scores represent the percentage of maximum achievable performance within each cognitive domain. The overall score is a composite of all eight domain scores. Performance tiers (Distinguished, High, Moderate, Developing) are determined by fixed thresholds applied uniformly across all participants.",
        ),
        MethodologySection(
            title="Interpretive Boundaries",
            content="Cognitive profiles describe patterns of assessed performance at the time of assessment. They do not represent fixed traits or permanent capacities. Cognitive performance is influenced by factors including fatigue, motivation, and environmental conditions. This assessment should be interpreted as one data point within a broader understanding of cognitive capacity.",
        ),
        MethodologySection(
            title="Limitations",
            content="This assessment does not diagnose clinical conditions, predict life outcomes, or assign inherent worth. It provides a structured description of cognitive performance across defined domains. Results should not be used as the sole basis for significant decisions about individuals.",
        ),
    ]


# --- Chart data builders --------------------------------------------------

def _build_constellation_data(assessment: AssessmentData) -> dict:
    points = []
    for i, d in enumerate(assessment.domains):
        angle = (i / len(assessment.domains)) * 2 * math.pi - math.pi / 2
        radius = (d.score / 100) * 0.85
        points.append({
            "name": DOMAIN_DISPLAY_NAMES[d.name],
            "value": d.score,
            "color": DOMAIN_SEMANTIC_COLORS[d.name],
            "x": math.cos(angle) * radius,
            "y": math.sin(angle) * radius,
            "domain": d.name.value,
        })

    # Connections between domains
    connections = []
    for i in range(len(assessment.domains)):
        for j in range(i + 1, len(assessment.domains)):
            d1, d2 = assessment.domains[i], assessment.domains[j]
            similarity = 1 - abs(d1.score - d2.score) / 100
            if similarity > 0.7:
                connections.append({
                    "from": i,
                    "to": j,
                    "strength": round(similarity, 3),
                })

    return {"points": points, "connections": connections}


def _build_radar_data(assessment: AssessmentData) -> dict:
    indicators = [{"name": DOMAIN_DISPLAY_NAMES[d.name], "max": 100} for d in assessment.domains]
    values = [d.score for d in assessment.domains]
    colors = [DOMAIN_SEMANTIC_COLORS[d.name] for d in assessment.domains]
    return {"indicators": indicators, "values": values, "colors": colors}


def _build_parallel_data(assessment: AssessmentData) -> dict:
    dimensions = [{"name": DOMAIN_DISPLAY_NAMES[d.name], "min": 0, "max": 100} for d in assessment.domains]
    values = [d.score for d in assessment.domains]
    colors = [DOMAIN_SEMANTIC_COLORS[d.name] for d in assessment.domains]
    return {"dimensions": dimensions, "values": values, "colors": colors}


# ---------------------------------------------------------------------------
# Main transformer
# ---------------------------------------------------------------------------

class CognitiveTransformer:
    def process(self, report: PsychometricReport) -> ProcessedReport:
        assessment = report.assessment
        sorted_d = sorted(assessment.domains, key=lambda d: d.score, reverse=True)

        pattern_insights, pattern_summary = _build_pattern_insights(assessment)

        return ProcessedReport(
            metadata=report.metadata,
            assessment=assessment,
            brain_mapping_asset=report.brain_mapping_asset,

            # Page 1
            cover_tagline=_build_cover_tagline(assessment),

            # Page 2
            highlight_badges=_build_highlight_badges(assessment),
            overview_summary=_build_overview_summary(assessment),

            # Page 3
            executive_summary=_build_executive_summary(assessment),

            # Page 4
            performance_overview=_build_performance_overview(assessment),

            # Page 5
            brain_associations=_build_brain_associations(assessment),

            # Page 6
            domain_cards=_build_domain_cards(assessment),

            # Page 7
            pattern_insights=pattern_insights,
            pattern_summary=pattern_summary,

            # Page 8
            persona=_build_persona(assessment),

            # Page 9
            interpersonal_insights=_build_interpersonal_insights(assessment),

            # Page 10
            development_stages=_build_development_stages(assessment),

            # Page 11
            recommended_labs=_build_recommended_labs(assessment),

            # Page 12
            methodology_sections=_build_methodology(),

            # Page 13
            closing_statement="Your cognitive profile is a living map, not a fixed destination.",
            closing_tagline="Continue exploring. Continue developing. Continue becoming.",

            # Chart data
            constellation_chart_data=_build_constellation_data(assessment),
            radar_chart_data=_build_radar_data(assessment),
            parallel_coordinates_data=_build_parallel_data(assessment),
        )
