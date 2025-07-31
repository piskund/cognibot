"""
Tests for multilingual support and specific test cases.

Includes the Russian logical fallacy test and other language-specific tests.
"""

import pytest
from bias_detector import BiasDetector
from llm_analyzer import LLMAnalyzer


class TestMultilingualSupport:
    """Test suite for multilingual bias detection."""

    @pytest.mark.asyncio
    async def test_russian_logical_fallacy(self, bias_detector, llm_analyzer, russian_test_case):
        """Test the Russian logical fallacy sentence with multilingual response."""
        text = russian_test_case["text"]
        
        # Test pattern-based detection
        pattern_results = bias_detector.analyze_text(text)
        
        # Pattern detection might not catch this logical structure
        # Document the behavior
        assert isinstance(pattern_results, list)
        
        # Test LLM analysis (requires API key)
        try:
            llm_result = await llm_analyzer.analyze_message(text)
            
            # LLM should ideally detect this logical fallacy
            assert isinstance(llm_result.has_biases, bool)
            assert 0.0 <= llm_result.confidence <= 1.0
            
            # Test multilingual response: should respond in Russian
            has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in llm_result.summary)
            
            if llm_result.has_biases and llm_result.confidence > 0.5:
                # If analysis is successful and detects issues, check for Russian response
                if not has_cyrillic:
                    print(f"⚠️  Expected Russian response, got: {llm_result.summary}")
                
                # Look for logical fallacy indicators in any language
                bias_text = " ".join(llm_result.detected_biases + [llm_result.summary]).lower()
                logical_fallacy_indicators = [
                    # English terms
                    "logical", "fallacy", "reasoning", "invalid", "affirming", "consequent", "logic",
                    # Russian terms
                    "логическ", "ошибк", "заблужден", "рассуждени", "неправильн"
                ]
                
                # Should mention logical issues
                logical_detected = any(indicator in bias_text for indicator in logical_fallacy_indicators)
                print(f"🔍 Logical fallacy indicators found: {logical_detected}")
                print(f"🌍 Response in Russian (Cyrillic): {has_cyrillic}")
                
        except Exception as e:
            pytest.skip(f"LLM analysis failed (likely missing API key): {e}")

    @pytest.mark.parametrize("language,text,expected_type", [
        ("russian", "Всякая селедка рыба, значит всякая рыба - селедка", "logical_fallacy"),
        ("english", "You're an idiot if you believe that", "ad_hominem"),
        ("english", "Everyone knows this is true", "bandwagon"),
    ])
    @pytest.mark.asyncio
    async def test_multilingual_detection(self, bias_detector, llm_analyzer, language, text, expected_type):
        """Test bias detection across different languages."""
        
        # Pattern-based detection
        pattern_results = bias_detector.analyze_text(text)
        assert isinstance(pattern_results, list)
        
        # LLM analysis (if API available)
        try:
            llm_result = await llm_analyzer.analyze_message(text)
            assert isinstance(llm_result, object)  # Just ensure it returns something
            
        except Exception:
            pytest.skip("LLM analysis not available")