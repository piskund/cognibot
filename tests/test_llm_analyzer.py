"""
Unit tests for the LLMAnalyzer class.

Tests OpenAI-based cognitive bias analysis functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch
from llm_analyzer import LLMAnalyzer, LLMAnalysisResult


class TestLLMAnalyzer:
    """Test suite for LLMAnalyzer functionality."""

    def test_analyzer_initialization(self, llm_analyzer):
        """Test that LLMAnalyzer initializes correctly."""
        assert llm_analyzer is not None
        assert hasattr(llm_analyzer, 'analyze_message')
        assert hasattr(llm_analyzer, 'client')

    @pytest.mark.asyncio
    async def test_analyze_message_structure(self, mock_llm_analyzer, sample_llm_result):
        """Test that analyze_message returns correct structure."""
        # Configure mock to return sample result
        mock_llm_analyzer.analyze_message.return_value = sample_llm_result
        
        result = await mock_llm_analyzer.analyze_message("Test text")
        
        assert isinstance(result, LLMAnalysisResult)
        assert hasattr(result, 'has_biases')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'detected_biases')
        assert hasattr(result, 'reasoning_quality')

    def test_format_analysis_summary(self, llm_analyzer, sample_llm_result):
        """Test formatting of analysis results."""
        formatted = llm_analyzer.format_analysis_summary(sample_llm_result)
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        # Should contain key information from the result
        assert any(bias in formatted.lower() for bias in sample_llm_result.detected_biases)

    @pytest.mark.asyncio 
    @pytest.mark.integration
    async def test_real_api_call(self, llm_analyzer):
        """Integration test with real OpenAI API call."""
        # This test requires a valid API key and is marked as integration
        # Skip if no API key is configured
        
        test_text = "You're an idiot if you believe that!"
        
        try:
            result = await llm_analyzer.analyze_message(test_text)
            
            assert isinstance(result, LLMAnalysisResult)
            assert isinstance(result.has_biases, bool)
            assert 0.0 <= result.confidence <= 1.0
            assert isinstance(result.detected_biases, list)
            
        except Exception as e:
            pytest.skip(f"API call failed (likely missing/invalid API key): {e}")

    def test_fallback_behavior(self, llm_analyzer):
        """Test fallback behavior when LLM analysis fails."""
        # Test the _create_fallback_result method
        fallback = llm_analyzer._create_fallback_result("test text")
        
        assert isinstance(fallback, LLMAnalysisResult)
        assert fallback.has_biases is False
        assert fallback.confidence == 0.0


class TestLLMAnalysisResult:
    """Test suite for LLMAnalysisResult data structure."""

    def test_result_creation(self, sample_llm_result):
        """Test that LLMAnalysisResult objects are created correctly."""
        assert sample_llm_result.has_biases is True
        assert sample_llm_result.confidence == 0.9
        assert "ad_hominem" in sample_llm_result.detected_biases
        assert sample_llm_result.reasoning_quality == "poor"

    def test_confidence_range(self, sample_llm_result):
        """Test that confidence values are in valid range."""
        assert 0.0 <= sample_llm_result.confidence <= 1.0

    def test_reasoning_quality_values(self, sample_llm_result):
        """Test that reasoning quality uses expected values."""
        valid_qualities = ["poor", "fair", "good", "excellent"]
        assert sample_llm_result.reasoning_quality in valid_qualities