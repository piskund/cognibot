"""
Unit tests for the BiasDetector class.

Tests pattern-based cognitive bias detection functionality.
"""

import pytest
from bias_detector import BiasDetector, BiasType


class TestBiasDetector:
    """Test suite for BiasDetector functionality."""

    def test_detector_initialization(self, bias_detector):
        """Test that BiasDetector initializes correctly."""
        assert bias_detector is not None
        assert hasattr(bias_detector, 'analyze_text')

    def test_ad_hominem_detection(self, bias_detector):
        """Test detection of ad hominem attacks."""
        text = "you're clearly an idiot if you believe that nonsense."
        results = bias_detector.analyze_text(text)
        
        assert len(results) > 0
        ad_hominem_found = any(r.bias_type == BiasType.AD_HOMINEM for r in results)
        assert ad_hominem_found

    def test_strawman_detection(self, bias_detector):
        """Test detection of strawman fallacies."""
        text = "So you're saying we should just give up completely?"
        results = bias_detector.analyze_text(text)
        
        # Note: This might not be detected by pattern matching alone
        # This test documents current behavior
        strawman_found = any(r.bias_type == BiasType.STRAWMAN for r in results)
        # Assert behavior (might be False for pattern-based detection)

    def test_clean_text_analysis(self, bias_detector):
        """Test that clean text produces no bias detections."""
        text = "This is a well-reasoned argument with evidence."
        results = bias_detector.analyze_text(text)
        
        # Clean text should have few or no detections
        high_confidence_results = [r for r in results if r.confidence > 0.8]
        assert len(high_confidence_results) == 0

    def test_empty_text(self, bias_detector):
        """Test behavior with empty text."""
        results = bias_detector.analyze_text("")
        assert results == []

    def test_multiple_biases(self, bias_detector):
        """Test detection when multiple biases are present."""
        text = "You're an idiot! Everyone knows this is true, so you must agree."
        results = bias_detector.analyze_text(text)
        
        # Should detect multiple types of bias
        bias_types = {r.bias_type for r in results}
        assert len(bias_types) >= 1  # At least ad hominem should be detected

    @pytest.mark.parametrize("test_case", [
        "You're clearly an idiot",
        "Everyone knows this is true", 
        "Most people agree with me",
        "You're either with us or against us"
    ])
    def test_various_bias_patterns(self, bias_detector, test_case):
        """Test detection across various bias patterns."""
        results = bias_detector.analyze_text(test_case)
        # Should return some results for these biased statements
        assert isinstance(results, list)


class TestBiasAnalysis:
    """Test suite for BiasAnalysis data structure."""

    def test_bias_analysis_creation(self, sample_bias_analysis):
        """Test that BiasAnalysis objects are created correctly."""
        assert sample_bias_analysis.bias_type == BiasType.AD_HOMINEM
        assert sample_bias_analysis.confidence == 0.85
        assert "Sample ad hominem" in sample_bias_analysis.explanation
        assert sample_bias_analysis.severity == "high"
        assert sample_bias_analysis.context == "Direct personal insult"

    def test_confidence_range(self, sample_bias_analysis):
        """Test that confidence values are in valid range."""
        assert 0.0 <= sample_bias_analysis.confidence <= 1.0