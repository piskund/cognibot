"""
Cognitive Bias Detection Module for CogniBot

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class BiasType(Enum):
    """Types of cognitive biases and logical errors."""
    CONFIRMATION_BIAS = "confirmation_bias"
    AD_HOMINEM = "ad_hominem"
    STRAWMAN = "strawman"
    FALSE_DICHOTOMY = "false_dichotomy"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    BANDWAGON = "bandwagon"
    SLIPPERY_SLOPE = "slippery_slope"
    CIRCULAR_REASONING = "circular_reasoning"
    HASTY_GENERALIZATION = "hasty_generalization"
    SURVIVORSHIP_BIAS = "survivorship_bias"
    ANCHORING_BIAS = "anchoring_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"

@dataclass
class BiasAnalysis:
    """Result of bias analysis."""
    bias_type: BiasType
    confidence: float
    explanation: str
    severity: str  # "low", "medium", "high"
    context: str

class BiasDetector:
    """Detects cognitive biases and logical errors in text."""
    
    def __init__(self):
        self.bias_patterns = self._initialize_patterns()
        self.bias_descriptions = self._initialize_descriptions()
    
    def _initialize_patterns(self) -> Dict[BiasType, List[str]]:
        """Initialize regex patterns for detecting biases."""
        return {
            BiasType.AD_HOMINEM: [
                r"you're (stupid|idiot|moron|dumb)",
                r"only an? (idiot|fool|moron) would",
                r"coming from someone who",
                r"you clearly don't understand",
            ],
            BiasType.STRAWMAN: [
                r"so you're saying",
                r"what you really mean is",
                r"if we follow your logic",
                r"by that logic",
            ],
            BiasType.FALSE_DICHOTOMY: [
                r"either .+ or .+, there's no middle ground",
                r"you're either .+ or .+",
                r"if you're not .+, then you must be .+",
            ],
            BiasType.APPEAL_TO_AUTHORITY: [
                r"experts say",
                r"studies show",
                r"scientists agree",
                r"according to \[famous person\]",
            ],
            BiasType.BANDWAGON: [
                r"everyone knows",
                r"most people agree",
                r"it's common knowledge",
                r"everybody does it",
            ],
        }
    
    def _initialize_descriptions(self) -> Dict[BiasType, str]:
        """Initialize descriptions for each bias type."""
        return {
            BiasType.CONFIRMATION_BIAS: "Tendency to search for, interpret, and recall information that confirms pre-existing beliefs",
            BiasType.AD_HOMINEM: "Attacking the person making an argument rather than the argument itself",
            BiasType.STRAWMAN: "Misrepresenting someone's argument to make it easier to attack",
            BiasType.FALSE_DICHOTOMY: "Presenting only two options when more exist",
            BiasType.APPEAL_TO_AUTHORITY: "Using authority as evidence without proper justification",
            BiasType.BANDWAGON: "Believing something because many others believe it",
            BiasType.SLIPPERY_SLOPE: "Assuming one event will lead to a chain of negative consequences",
            BiasType.CIRCULAR_REASONING: "Using the conclusion as evidence for the premise",
            BiasType.HASTY_GENERALIZATION: "Drawing broad conclusions from limited examples",
            BiasType.SURVIVORSHIP_BIAS: "Focusing on successful examples while ignoring failures",
            BiasType.ANCHORING_BIAS: "Over-relying on the first piece of information encountered",
            BiasType.AVAILABILITY_HEURISTIC: "Overestimating likelihood based on memorable examples",
        }
    
    def analyze_text(self, text: str) -> List[BiasAnalysis]:
        """Analyze text for cognitive biases and logical errors."""
        results = []
        text_lower = text.lower()
        
        # Pattern-based detection
        for bias_type, patterns in self.bias_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    confidence = self._calculate_confidence(bias_type, match.group(), text)
                    if confidence > 0.5:  # Threshold for reporting
                        results.append(BiasAnalysis(
                            bias_type=bias_type,
                            confidence=confidence,
                            explanation=self.bias_descriptions[bias_type],
                            severity=self._determine_severity(confidence),
                            context=self._extract_context(text, match.start(), match.end())
                        ))
        
        return results
    
    def _calculate_confidence(self, bias_type: BiasType, match_text: str, full_text: str) -> float:
        """Calculate confidence score for detected bias."""
        base_confidence = 0.6
        
        # Adjust based on context
        if len(full_text.split()) < 10:
            base_confidence -= 0.2  # Less confident in short texts
        
        # Bias-specific adjustments
        if bias_type == BiasType.AD_HOMINEM:
            if any(word in full_text.lower() for word in ['argument', 'point', 'claim']):
                base_confidence += 0.2
        
        return min(1.0, max(0.0, base_confidence))
    
    def _determine_severity(self, confidence: float) -> str:
        """Determine severity level based on confidence."""
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _extract_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Extract context around the detected bias."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def generate_summary(self, analyses: List[BiasAnalysis]) -> str:
        """Generate a summary of detected biases."""
        if not analyses:
            return "No significant cognitive biases or logical errors detected."
        
        summary_parts = []
        bias_counts = {}
        
        for analysis in analyses:
            bias_name = analysis.bias_type.value.replace('_', ' ').title()
            bias_counts[bias_name] = bias_counts.get(bias_name, 0) + 1
        
        summary_parts.append("🧠 **Cognitive Bias Analysis:**\n")
        
        for bias_name, count in bias_counts.items():
            summary_parts.append(f"• **{bias_name}** ({count} instance{'s' if count > 1 else ''})")
        
        # Add highest confidence finding
        highest_confidence = max(analyses, key=lambda x: x.confidence)
        summary_parts.append(f"\n🎯 **Most Significant Issue:**")
        summary_parts.append(f"**{highest_confidence.bias_type.value.replace('_', ' ').title()}** (Confidence: {highest_confidence.confidence:.0%})")
        summary_parts.append(f"*{highest_confidence.explanation}*")
        
        return "\n".join(summary_parts) 