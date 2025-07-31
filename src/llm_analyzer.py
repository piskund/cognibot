"""
LLM Analysis Module for CogniBot - OpenAI Integration

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

import asyncio
from typing import Dict, List, Optional
import openai
from openai import AsyncOpenAI
from dataclasses import dataclass
import json
from loguru import logger

from config import settings
from bias_detector import BiasAnalysis, BiasType

@dataclass
class LLMAnalysisResult:
    """Result from LLM analysis."""
    has_biases: bool
    confidence: float
    detected_biases: List[str]
    reasoning_quality: str  # "poor", "fair", "good", "excellent"
    discussion_issues: List[str]
    suggestions: List[str]
    summary: str

class LLMAnalyzer:
    """Uses LLM to analyze text for cognitive biases and logical errors."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.analysis_prompt = self._create_analysis_prompt()
    
    def _create_analysis_prompt(self) -> str:
        """Create the system prompt for bias analysis."""
        return """You are an expert in cognitive psychology, logic, and critical thinking. Analyze the given text for:

1. **Cognitive Biases**: Confirmation bias, availability heuristic, anchoring bias, etc.
2. **Logical Fallacies**: Ad hominem, strawman, false dichotomy, slippery slope, etc.
3. **Discussion Quality**: Constructive vs destructive patterns, evidence usage, respectful discourse
4. **Reasoning Errors**: Hasty generalizations, circular reasoning, etc.

Respond in JSON format with the following structure:
{
    "has_biases": boolean,
    "confidence": float (0.0-1.0),
    "detected_biases": ["bias1", "bias2", ...],
    "reasoning_quality": "poor|fair|good|excellent",
    "discussion_issues": ["issue1", "issue2", ...],
    "suggestions": ["suggestion1", "suggestion2", ...],
    "summary": "Brief explanation of findings"
}

Focus on:
- Clear evidence of biased thinking
- Logical structure and validity
- Respectful vs hostile communication
- Use of evidence and sources
- Open-mindedness vs dogmatism

Be constructive and educational in your analysis."""

    async def analyze_message(self, text: str, context: Optional[str] = None) -> LLMAnalysisResult:
        """Analyze a message using LLM for cognitive biases and discussion quality."""
        try:
            # Prepare the user message
            user_message = f"Text to analyze: {text}"
            if context:
                user_message += f"\n\nContext: {context}"
            
            # Make API call
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.analysis_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content
            result_data = json.loads(content)
            
            return LLMAnalysisResult(
                has_biases=result_data.get("has_biases", False),
                confidence=result_data.get("confidence", 0.0),
                detected_biases=result_data.get("detected_biases", []),
                reasoning_quality=result_data.get("reasoning_quality", "fair"),
                discussion_issues=result_data.get("discussion_issues", []),
                suggestions=result_data.get("suggestions", []),
                summary=result_data.get("summary", "Analysis completed.")
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._create_fallback_result(text)
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return self._create_fallback_result(text)
    
    def _create_fallback_result(self, text: str) -> LLMAnalysisResult:
        """Create a fallback result when LLM analysis fails."""
        return LLMAnalysisResult(
            has_biases=False,
            confidence=0.0,
            detected_biases=[],
            reasoning_quality="unknown",
            discussion_issues=[],
            suggestions=["Unable to analyze due to technical issues"],
            summary="Analysis could not be completed."
        )
    
    async def generate_educational_response(self, analysis: LLMAnalysisResult, original_text: str) -> str:
        """Generate an educational response about detected biases."""
        if not analysis.has_biases and not analysis.discussion_issues:
            return None
        
        try:
            prompt = f"""Based on this analysis of a message, create a brief, educational response that:
1. Points out the cognitive biases or logical issues found
2. Explains WHY these are problematic
3. Suggests better ways to make the same point
4. Is respectful and constructive

Analysis results:
- Detected biases: {', '.join(analysis.detected_biases)}
- Discussion issues: {', '.join(analysis.discussion_issues)}
- Reasoning quality: {analysis.reasoning_quality}

Original message: {original_text[:500]}...

Create a response that's educational, not confrontational. Focus on helping improve discourse quality."""

            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful educator focused on improving critical thinking and discourse quality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failed to generate educational response: {e}")
            return None
    
    def format_analysis_summary(self, analysis: LLMAnalysisResult) -> str:
        """Format the analysis results into a readable summary."""
        if not analysis.has_biases and not analysis.discussion_issues:
            return "✅ **Good Discussion Quality**: No significant cognitive biases or logical errors detected."
        
        summary_parts = []
        
        # Header with confidence
        confidence_emoji = "🔴" if analysis.confidence > 0.8 else "🟡" if analysis.confidence > 0.5 else "🟢"
        summary_parts.append(f"{confidence_emoji} **Cognitive Bias Analysis** (Confidence: {analysis.confidence:.0%})")
        
        # Detected biases
        if analysis.detected_biases:
            summary_parts.append("\n🧠 **Detected Issues:**")
            for bias in analysis.detected_biases:
                summary_parts.append(f"• {bias}")
        
        # Discussion quality
        quality_emoji = {"poor": "❌", "fair": "⚠️", "good": "✅", "excellent": "🌟"}.get(analysis.reasoning_quality, "❓")
        summary_parts.append(f"\n{quality_emoji} **Reasoning Quality:** {analysis.reasoning_quality.title()}")
        
        # Discussion issues
        if analysis.discussion_issues:
            summary_parts.append("\n⚠️ **Discussion Issues:**")
            for issue in analysis.discussion_issues:
                summary_parts.append(f"• {issue}")
        
        # Suggestions
        if analysis.suggestions and len(analysis.suggestions) <= 3:  # Limit suggestions
            summary_parts.append("\n💡 **Suggestions:**")
            for suggestion in analysis.suggestions[:3]:
                summary_parts.append(f"• {suggestion}")
        
        # Summary
        if analysis.summary:
            summary_parts.append(f"\n📝 **Summary:** {analysis.summary}")
        
        return "\n".join(summary_parts) 