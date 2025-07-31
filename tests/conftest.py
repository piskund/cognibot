"""
Pytest configuration and shared fixtures for CogniBot tests.

This module provides common setup, fixtures, and utilities used across all tests.
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add src directory to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Import after path setup
from bias_detector import BiasDetector, BiasAnalysis, BiasType
from llm_analyzer import LLMAnalyzer, LLMAnalysisResult


@pytest.fixture
def bias_detector():
    """Fixture providing a BiasDetector instance."""
    return BiasDetector()


@pytest.fixture  
def llm_analyzer():
    """Fixture providing an LLMAnalyzer instance."""
    return LLMAnalyzer()


@pytest.fixture
def mock_llm_analyzer():
    """Fixture providing a mocked LLMAnalyzer for testing without API calls."""
    analyzer = MagicMock(spec=LLMAnalyzer)
    analyzer.analyze_message = AsyncMock()
    analyzer.format_analysis_summary = MagicMock()
    return analyzer


@pytest.fixture
def sample_bias_analysis():
    """Fixture providing a sample BiasAnalysis for testing."""
    return BiasAnalysis(
        bias_type=BiasType.AD_HOMINEM,
        confidence=0.85,
        explanation="Sample ad hominem attack detected",
        severity="high",
        context="Direct personal insult"
    )


@pytest.fixture
def sample_llm_result():
    """Fixture providing a sample LLMAnalysisResult for testing."""
    return LLMAnalysisResult(
        has_biases=True,
        confidence=0.9,
        detected_biases=["ad_hominem", "logical_fallacy"],
        reasoning_quality="poor",
        discussion_issues=["hostile_tone", "invalid_logic"],
        suggestions=["Use respectful language", "Provide evidence"],
        summary="Text contains personal attacks and logical errors",
        api_error=None,
        error_message=None
    )


# Test data fixtures
@pytest.fixture
def test_messages():
    """Fixture providing test messages with expected biases."""
    return [
        {
            "text": "You're clearly an idiot if you believe that. Only a moron would think otherwise.",
            "expected_biases": ["ad_hominem"],
            "description": "Clear ad hominem attack"
        },
        {
            "text": "So you're saying we should just give up completely? That's not what I meant at all.",
            "expected_biases": ["strawman"],
            "description": "Strawman fallacy example"
        },
        {
            "text": "Everyone knows this is true. Most people agree with this statement.",
            "expected_biases": ["bandwagon"],
            "description": "Bandwagon fallacy (appeal to popularity)"
        },
        {
            "text": "You're either with us or against us. There's no middle ground on this issue.",
            "expected_biases": ["false_dichotomy"],
            "description": "False dichotomy fallacy"
        },
        {
            "text": "This is a well-reasoned argument with good evidence and respectful tone.",
            "expected_biases": [],
            "description": "Clean text without biases"
        }
    ]


@pytest.fixture
def russian_test_case():
    """Fixture providing the Russian logical fallacy test case."""
    return {
        "text": "Всякая селедка рыба, значит всякая рыба - селедка",
        "translation": "Every herring is a fish, therefore every fish is a herring",
        "expected_fallacy": "affirming_the_consequent",
        "description": "Russian logical fallacy example"
    }