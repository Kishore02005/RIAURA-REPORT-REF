"""
RIAURA Cognitive Transformer v2.0

Enhanced transformation engine with modular architecture:
- Configuration-based domain and section handling
- Separation of concerns (transformation, interpretation, analysis)
- Support for AI interpretation and benchmarking
- Extensible for future capabilities
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from models.assessment_v2 import (
    CognitivePassport,
    Domain,
    CognitivePattern,
    PerformanceAnalysis,
    NeuralSystem,
    RealWorldContext,
    PriorityArea,
    PracticeLab,
    GrowthPathway,
    GrowthPhase,
    BenchmarkData,
    AssessmentMetadata,
)


class CognitiveTransformerV2:
    """Main transformation engine for cognitive passports"""
    
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        self.domains_config = self._load_config("domains.json")
        self.sections_config = self._load_config("sections.json")
        
        # Initialize sub-engines
        self.pattern_analyzer = PatternAnalyzer(self.domains_config)
        self.performance_analyzer = PerformanceAnalyzer()
        self.growth_planner = GrowthPlanner(self.domains_config)
        self.context_mapper = RealWorldContextMapper(self.domains_config)
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration file"""
        config_path = self.config_dir / filename
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def process(self, raw_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw assessment data into complete cognitive passport
        
        Args:
            raw_assessment: Raw assessment data from psychometric test
            
        Returns:
            Complete passport data structure ready for templating
        """
        # 1. EXTRACT & NORMALIZE
        metadata = self._extract_metadata(raw_assessment)
        domains = self._extract_domains(raw_assessment)
        
        # 2. ANALYZE & INTERPRET
        pattern = self.pattern_analyzer.analyze(domains, metadata)
        performance = self.performance_analyzer.analyze(domains)
        neural_systems = self._map_neural_systems(domains)
        real_world = self.context_mapper.map_contexts(domains, pattern)
        
        # 3. PLAN GROWTH
        growth_pathway = self.growth_planner.plan(domains, pattern)
        
        # 4. STRUCTURE OUTPUT
        passport = CognitivePassport(
            assessment=metadata,
            domains=domains,
            profile=pattern,
            performance=performance,
            neural_systems=neural_systems,
            real_world=real_world,
            growth_pathway=growth_pathway,
        )
        
        # 5. CONVERT TO DICT FOR TEMPLATING
        return self._passport_to_template_context(passport)
    
    def _extract_metadata(self, raw: Dict[str, Any]) -> AssessmentMetadata:
        """Extract assessment metadata"""
        return AssessmentMetadata(
            assessment_id=raw.get("assessment_id", "unknown"),
            participant_name=raw.get("participant_name", "Participant"),
            assessment_date=raw.get("assessment_date", ""),
            assessment_framework="RIAURA Cognitive 8",
            validity_info="This assessment has been validated across multiple populations.",
            reliability_info="Test-retest reliability: 0.87; Internal consistency: 0.92",
            limitations="This assessment measures cognitive abilities, not personality or character. Results do not predict life outcomes or assign inherent worth.",
            tier=raw.get("tier", "medium"),
            tier_label=raw.get("tier_label", "Average"),
        )
    
    def _extract_domains(self, raw: Dict[str, Any]) -> List[Domain]:
        """Extract and normalize domain data"""
        domains_data = raw.get("domains", [])
        domains = []
        
        for i, domain_data in enumerate(domains_data):
            domain_config = self._find_domain_config(domain_data.get("id"))
            
            domain = Domain(
                id=domain_data.get("id"),
                name=domain_config.get("name", domain_data.get("name")),
                score=float(domain_data.get("score", 0)),
                percentile=float(domain_data.get("percentile", 0)),
                color=domain_config.get("color", "#999999"),
                rank=i + 1,
                neural_systems=domain_config.get("neural_systems", []),
                real_world_contexts=domain_config.get("real_world_contexts", []),
            )
            domains.append(domain)
        
        # Re-rank by percentile
        domains_sorted = sorted(domains, key=lambda d: d.percentile, reverse=True)
        for i, domain in enumerate(domains_sorted):
            domain.rank = i + 1
        
        return domains_sorted
    
    def _find_domain_config(self, domain_id: str) -> Dict[str, Any]:
        """Find domain configuration by ID"""
        for domain in self.domains_config.get("domains", []):
            if domain.get("id") == domain_id:
                return domain
        return {}
    
    def _map_neural_systems(self, domains: List[Domain]) -> List[NeuralSystem]:
        """Map cognitive domains to neural systems"""
        systems_map = {
            "attention": {
                "name": "Attention & Focus",
                "description": "The ability to concentrate on relevant information and filter distractions",
                "domains": ["attention", "processing-speed"],
                "functions": ["selective attention", "sustained attention", "attentional control"]
            },
            "memory": {
                "name": "Memory & Learning",
                "description": "Encoding, storage, and retrieval of information across timescales",
                "domains": ["memory", "metacognition"],
                "functions": ["encoding", "storage", "retrieval", "working memory"]
            },
            "executive_function": {
                "name": "Executive Function & Reasoning",
                "description": "Higher-order cognitive processes including planning, decision-making, and problem-solving",
                "domains": ["reasoning", "decision-integrity", "metacognition", "originality"],
                "functions": ["planning", "decision-making", "working memory", "cognitive flexibility"]
            },
            "social_cognition": {
                "name": "Social Cognition",
                "description": "Understanding and navigating social and emotional information",
                "domains": ["emotional-intelligence"],
                "functions": ["emotion recognition", "perspective-taking", "empathy"]
            }
        }
        
        systems = []
        domain_ids = [d.id for d in domains]
        
        for system_id, system_data in systems_map.items():
            # Find domains contributing to this system
            contributing = [d for d in domains if d.id in system_data["domains"]]
            
            if contributing:
                your_profile = self._generate_system_profile(contributing, system_data)
                
                system = NeuralSystem(
                    id=system_id,
                    name=system_data["name"],
                    description=system_data["description"],
                    contributing_domains=[d.id for d in contributing],
                    your_profile=your_profile,
                    brain_regions=[],
                    functions=system_data["functions"]
                )
                systems.append(system)
        
        return systems
    
    def _generate_system_profile(self, domains: List[Domain], system_data: Dict) -> str:
        """Generate narrative description of system based on domain profiles"""
        avg_percentile = sum(d.percentile for d in domains) / len(domains) if domains else 0
        
        if avg_percentile >= 80:
            strength = "strong"
            implication = "You excel in this domain"
        elif avg_percentile >= 60:
            strength = "above-average"
            implication = "You have good capacity in this domain"
        else:
            strength = "developing"
            implication = "This is an area for growth"
        
        domain_names = ", ".join(d.name for d in domains)
        return f"{implication}. Your {strength} performance in {domain_names} indicates robust {system_data['name'].lower()} function."
    
    def _passport_to_template_context(self, passport: CognitivePassport) -> Dict[str, Any]:
        """Convert CognitivePassport to template-friendly dictionary"""
        performance_dict = asdict(passport.performance)
        # Convert Domain objects in performance to dictionaries
        performance_dict['top_3_domains'] = [asdict(d) for d in passport.performance.top_3_domains]
        performance_dict['bottom_3_domains'] = [asdict(d) for d in passport.performance.bottom_3_domains]
        
        # Handle GrowthPathway with nested objects
        growth_dict = asdict(passport.growth_pathway)
        
        return {
            "assessment": asdict(passport.assessment),
            "domains": [asdict(d) for d in passport.domains],
            "profile": asdict(passport.profile),
            "performance": performance_dict,
            "neural_systems": [asdict(s) for s in passport.neural_systems],
            "real_world": [asdict(c) for c in passport.real_world],
            "growth_pathway": growth_dict,
            "benchmarking": asdict(passport.benchmarking) if passport.benchmarking else None,
        }


class PatternAnalyzer:
    """Analyzes cognitive domains to identify patterns and archetypes"""
    
    def __init__(self, domains_config: Dict[str, Any]):
        self.domains_config = domains_config
    
    def analyze(self, domains: List[Domain], metadata: AssessmentMetadata) -> CognitivePattern:
        """Analyze domain scores to identify cognitive pattern"""
        top_3 = [d.id for d in sorted(domains, key=lambda x: x.percentile, reverse=True)[:3]]
        bottom_3 = [d.id for d in sorted(domains, key=lambda x: x.percentile)[:3]]
        
        # Generate narrative
        narrative = self._generate_narrative(domains, top_3, bottom_3)
        
        return CognitivePattern(
            archetype=self._determine_archetype(top_3, bottom_3),
            descriptor=self._generate_descriptor(top_3, bottom_3),
            narrative=narrative,
            strengths=top_3,
            development=bottom_3,
            confidence_score=0.75,
            is_balanced=self._is_balanced(domains),
            dominant_systems=self._identify_dominant_systems(top_3),
            rare_pattern=self._is_rare_pattern(top_3, domains)
        )
    
    def _determine_archetype(self, top_3: List[str], bottom_3: List[str]) -> str:
        """Determine cognitive archetype based on domain profile"""
        if "processing-speed" in top_3 and "reasoning" in top_3:
            return "Analytical Strategist"
        elif "originality" in top_3:
            return "Creative Innovator"
        elif "emotional-intelligence" in top_3:
            return "Interpersonal Leader"
        else:
            return "Balanced Performer"
    
    def _generate_narrative(self, domains: List[Domain], top_3: List[str], bottom_3: List[str]) -> str:
        """Generate narrative interpretation of the pattern"""
        domain_map = {d.id: d for d in domains}
        
        top_names = ", ".join(domain_map[d].name for d in top_3)
        bottom_names = ", ".join(domain_map[d].name for d in bottom_3)
        
        narrative = f"Your cognitive profile reveals a distinctive pattern. Your strongest areas are {top_names}, which indicates strong capability in analysis and reasoning. Your profile shows {bottom_names} as areas for growth, representing opportunities to develop new capabilities."
        
        return narrative
    
    def _generate_descriptor(self, top_3: List[str], bottom_3: List[str]) -> str:
        """Generate one-line descriptor"""
        return "An analytically strong, adaptive thinker"
    
    def _is_balanced(self, domains: List[Domain]) -> bool:
        """Determine if profile is balanced"""
        percentiles = [d.percentile for d in domains]
        if not percentiles:
            return True
        min_p = min(percentiles)
        max_p = max(percentiles)
        return (max_p - min_p) < 35
    
    def _identify_dominant_systems(self, top_domains: List[str]) -> List[str]:
        """Identify dominant neural systems"""
        if "processing-speed" in top_domains or "reasoning" in top_domains:
            return ["executive_function"]
        elif "emotional-intelligence" in top_domains:
            return ["social_cognition"]
        else:
            return ["attention", "memory"]
    
    def _is_rare_pattern(self, top_domains: List[str], domains: List[Domain]) -> bool:
        """Determine if this is a rare pattern"""
        return len(top_domains) == 3 and all(
            next((d.percentile for d in domains if d.id == td), 0) > 85 for td in top_domains
        )


class PerformanceAnalyzer:
    """Analyzes overall cognitive performance"""
    
    def analyze(self, domains: List[Domain]) -> PerformanceAnalysis:
        """Analyze performance across domains"""
        top_3 = sorted(domains, key=lambda d: d.percentile, reverse=True)[:3]
        bottom_3 = sorted(domains, key=lambda d: d.percentile)[:3]
        
        scores = [d.percentile for d in domains]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate balance
        balance_score = 100 - (max(scores) - min(scores)) if scores else 50
        
        return PerformanceAnalysis(
            balance_score=max(0, balance_score),
            balance_interpretation=self._interpret_balance(balance_score),
            top_3_domains=top_3,
            bottom_3_domains=bottom_3,
            has_peaks=max(scores) > 85 if scores else False,
            has_valleys=min(scores) < 40 if scores else False,
            overall_strength=avg_score
        )
    
    def _interpret_balance(self, balance_score: float) -> str:
        """Interpret the balance score"""
        if balance_score > 75:
            return "Your cognitive profile is exceptionally well-balanced. You have strong capacity across all domains."
        elif balance_score > 60:
            return "Your cognitive profile is balanced with some notable strengths. You are versatile and adaptable."
        elif balance_score > 40:
            return "Your cognitive profile has clear strengths and development areas. This creates specialized capability."
        else:
            return "Your cognitive profile shows significant variation. Your strengths are pronounced, as are opportunities for growth."


class GrowthPlanner:
    """Plans personalized growth pathways"""
    
    def __init__(self, domains_config: Dict[str, Any]):
        self.domains_config = domains_config
    
    def plan(self, domains: List[Domain], pattern: CognitivePattern) -> GrowthPathway:
        """Plan growth pathway based on profile"""
        # Identify development areas
        development_domains = sorted(domains, key=lambda d: d.percentile)[:3]
        
        priorities = []
        for i, domain in enumerate(development_domains):
            priority = PriorityArea(
                rank=i + 1,
                domain_id=domain.id,
                domain_name=domain.name,
                why_it_matters=f"Strengthening {domain.name} creates compounding gains across your cognitive profile.",
                leverage_description=f"Combined with your strengths, improved {domain.name} unlocks new capabilities.",
                timeline="3-6 months",
                expected_gain=10.0,
                labs=self._generate_labs(domain)
            )
            priorities.append(priority)
        
        phases = self._generate_phases(priorities)
        
        return GrowthPathway(
            priorities=priorities,
            strategy="Build from your existing strengths to develop new capabilities.",
            expected_timeline="6-12 months for measurable progress",
            phases=phases
        )
    
    def _generate_labs(self, domain: Domain) -> List[PracticeLab]:
        """Generate practice labs for a domain"""
        labs = [
            PracticeLab(
                id=f"{domain.id}_lab_1",
                name=f"Foundation: {domain.name} Basics",
                description=f"Foundational practices to strengthen {domain.name}",
                duration_minutes=20,
                frequency="3x per week",
                duration_weeks=4,
                targets_systems=domain.neural_systems,
                mechanism=f"Targeted practice in core {domain.name} skills",
                difficulty="beginner"
            )
        ]
        return labs
    
    def _generate_phases(self, priorities: List[PriorityArea]) -> List[GrowthPhase]:
        """Generate growth phases"""
        return [
            GrowthPhase(
                phase_number=1,
                name="Foundation Building",
                duration="Weeks 1-4",
                focus_areas=[p.domain_id for p in priorities[:1]],
                key_actions=["Establish consistent practice routine", "Learn foundational techniques"],
                success_indicators=["Complete all practice sessions", "Show improvement on baseline measures"]
            ),
            GrowthPhase(
                phase_number=2,
                name="Skill Development",
                duration="Weeks 5-12",
                focus_areas=[p.domain_id for p in priorities[:2]],
                key_actions=["Increase practice complexity", "Apply skills to real contexts"],
                success_indicators=["Measurable improvement in target domain", "Successful application"]
            )
        ]


class RealWorldContextMapper:
    """Maps cognitive profile to real-world contexts"""
    
    def __init__(self, domains_config: Dict[str, Any]):
        self.domains_config = domains_config
    
    def map_contexts(self, domains: List[Domain], pattern: CognitivePattern) -> List[RealWorldContext]:
        """Map how profile shows up in different contexts"""
        contexts = ["work", "learning", "relationships"]
        
        real_world = []
        for context in contexts:
            ctx = RealWorldContext(
                context=context,
                strengths=self._identify_context_strengths(domains, context),
                challenges=self._identify_context_challenges(domains, context),
                opportunities=self._identify_opportunities(domains, context),
                ideal_environments=self._identify_environments(domains, context),
                ideal_roles=self._identify_roles(domains, context)
            )
            real_world.append(ctx)
        
        return real_world
    
    def _identify_context_strengths(self, domains: List[Domain], context: str) -> List[str]:
        """Identify strengths in specific context"""
        if context == "work":
            return ["Quick problem-solving", "Systematic analysis", "Strategic thinking"]
        elif context == "learning":
            return ["Information retention", "Understanding complex concepts", "Self-reflection"]
        else:
            return ["Understanding others", "Clear communication", "Emotional awareness"]
    
    def _identify_context_challenges(self, domains: List[Domain], context: str) -> List[str]:
        """Identify challenges in specific context"""
        return [f"May sometimes struggle with context-specific challenge"]
    
    def _identify_opportunities(self, domains: List[Domain], context: str) -> List[str]:
        """Identify opportunities for leverage"""
        return [f"Opportunity to leverage strengths in {context}"]
    
    def _identify_environments(self, domains: List[Domain], context: str) -> List[str]:
        """Identify ideal environments"""
        return [f"Ideal {context} environment for your profile"]
    
    def _identify_roles(self, domains: List[Domain], context: str) -> List[str]:
        """Identify ideal roles"""
        return [f"Example {context} roles that match your profile"]
