"""
RIAURA Cognitive Assessment Data Models - Version 2.0

Enhanced data structures for modular, configuration-driven architecture.
Supports multiple assessment frameworks, longitudinal tracking, and AI interpretation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime


@dataclass
class Domain:
    """Represents a cognitive domain with scores and metadata"""
    id: str
    name: str
    score: float  # Raw score (0-100)
    percentile: float  # Percentile rank (0-100)
    color: str  # Hex color code
    rank: int  # Ranking among domains (1-8)
    
    # Neural correlates
    neural_systems: List[str] = field(default_factory=list)
    
    # Context mapping
    real_world_contexts: List[str] = field(default_factory=list)  # ["work", "learning", "relationships"]
    
    # Computed properties
    classification: Literal["very_high", "high", "above_average", "average", "below_average", "low"] = "average"
    
    def __post_init__(self):
        """Compute classification based on percentile"""
        if self.percentile >= 85:
            self.classification = "very_high"
        elif self.percentile >= 70:
            self.classification = "high"
        elif self.percentile >= 60:
            self.classification = "above_average"
        elif self.percentile >= 40:
            self.classification = "average"
        elif self.percentile >= 25:
            self.classification = "below_average"
        else:
            self.classification = "low"


@dataclass
class CognitivePattern:
    """Represents the overall cognitive pattern/archetype"""
    archetype: str  # e.g., "Analytical Strategist"
    descriptor: str  # One-line description
    narrative: str  # 2-3 paragraph interpretation
    strengths: List[str]  # Domain IDs of top 3 strengths
    development: List[str]  # Domain IDs of primary development areas
    confidence_score: float  # 0-1 confidence in pattern classification
    
    # Pattern characteristics
    is_balanced: bool = True
    dominant_systems: List[str] = field(default_factory=list)  # Neural systems
    rare_pattern: bool = False  # If <10% of population matches


@dataclass
class PerformanceAnalysis:
    """Analysis of overall cognitive performance"""
    balance_score: float  # 0-100, how balanced the profile is
    balance_interpretation: str  # Why this balance matters
    
    top_3_domains: List[Domain]  # Ranked highest 3
    bottom_3_domains: List[Domain]  # Ranked lowest 3
    
    # Performance characteristics
    has_peaks: bool = False
    has_valleys: bool = False
    overall_strength: float = 0.0  # Average score across domains


@dataclass
class NeuralSystem:
    """Represents a functional brain system"""
    id: str
    name: str
    description: str
    contributing_domains: List[str]  # Domain IDs that contribute to this system
    your_profile: str  # How this system manifests in the individual's profile
    
    # Neuroscience details
    brain_regions: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)


@dataclass
class RealWorldContext:
    """How cognitive profile shows up in specific life contexts"""
    context: Literal["work", "learning", "relationships"]
    strengths: List[str]  # How strengths manifest here
    challenges: List[str]  # How development areas manifest here
    opportunities: List[str]  # How to leverage strengths
    ideal_environments: List[str]  # Environments where this person thrives
    ideal_roles: List[str]  # Example roles that leverage profile


@dataclass
class PriorityArea:
    """A prioritized area for cognitive development"""
    rank: int  # 1-5 priority ranking
    domain_id: str
    domain_name: str
    
    # Why it matters
    why_it_matters: str  # Why this domain was selected as priority
    leverage_description: str  # How developing this creates compounding gains
    
    # Growth path
    timeline: str  # e.g., "3-6 months"
    expected_gain: float  # Expected percentile improvement (5-15)
    
    # Associated labs
    labs: List[PracticeLab] = field(default_factory=list)


@dataclass
class PracticeLab:
    """A specific practice activity targeting cognitive development"""
    id: str
    name: str
    description: str
    
    # Activity details
    duration_minutes: int
    frequency: str  # e.g., "3x per week"
    duration_weeks: int
    
    # Neuroscience
    targets_systems: List[str]  # Which neural systems this targets
    mechanism: str  # How this strengthens the domain
    
    # Progress tracking
    difficulty: Literal["beginner", "intermediate", "advanced"] = "beginner"
    prerequisite_labs: List[str] = field(default_factory=list)


@dataclass
class GrowthPathway:
    """Complete growth path for the individual"""
    priorities: List[PriorityArea]
    
    # Overall strategy
    strategy: str  # High-level approach to growth
    expected_timeline: str  # Total timeline for growth
    
    # Phases
    phases: List[GrowthPhase] = field(default_factory=list)


@dataclass
class GrowthPhase:
    """A phase in the growth pathway"""
    phase_number: int
    name: str  # e.g., "Foundation Building"
    duration: str  # e.g., "Weeks 1-4"
    focus_areas: List[str]  # Domain IDs to focus on
    key_actions: List[str]
    success_indicators: List[str]


@dataclass
class BenchmarkData:
    """Normative data and peer comparison"""
    percentile_rank: float  # Where user ranks in population
    population_context: str  # e.g., "Top 19% of assessments"
    
    # Pattern frequency
    pattern_frequency: float  # % of population with similar pattern
    similar_profiles: str  # Description of similar profiles
    
    # Domain benchmarks
    domain_benchmarks: Dict[str, float]  # Domain ID -> population average
    your_vs_population: Dict[str, str]  # Domain ID -> "above" | "average" | "below"


@dataclass
class AssessmentMetadata:
    """Metadata about the assessment"""
    assessment_id: str
    participant_name: str
    assessment_date: str
    
    # Validity information
    assessment_framework: str  # e.g., "RIAURA Cognitive 8"
    validity_info: str
    reliability_info: str
    limitations: str
    
    # Classification
    tier: Literal["low", "medium", "high", "very_high"]
    tier_label: str
    
    # Additional metadata
    demographics: Dict[str, str] = field(default_factory=dict)
    previous_assessment_id: Optional[str] = None


@dataclass
class CognitivePassport:
    """Complete cognitive passport report"""
    # Core assessment
    assessment: AssessmentMetadata
    
    # Profile components
    domains: List[Domain]
    profile: CognitivePattern
    performance: PerformanceAnalysis
    
    # Understanding layer
    neural_systems: List[NeuralSystem]
    real_world: List[RealWorldContext]
    
    # Action layer
    growth_pathway: GrowthPathway
    
    # Benchmarking (optional)
    benchmarking: Optional[BenchmarkData] = None
    
    # Historical data (optional)
    longitudinal_data: Optional[Dict[str, List[float]]] = None
    
    # AI interpretation (optional)
    ai_interpretation: Optional[Dict[str, str]] = None
    
    def get_domain_by_id(self, domain_id: str) -> Optional[Domain]:
        """Helper to find domain by ID"""
        return next((d for d in self.domains if d.id == domain_id), None)
    
    def get_top_domains(self, n: int = 3) -> List[Domain]:
        """Get top N domains by percentile"""
        return sorted(self.domains, key=lambda d: d.percentile, reverse=True)[:n]
    
    def get_development_areas(self, n: int = 3) -> List[Domain]:
        """Get bottom N domains by percentile"""
        return sorted(self.domains, key=lambda d: d.percentile)[:n]


# Type aliases for common patterns
DomainDict = Dict[str, float]
DomainScores = Dict[str, Domain]
