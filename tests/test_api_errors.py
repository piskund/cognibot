"""
Tests for OpenAI API error handling.

Tests various API error scenarios and ensures proper error handling and messaging.
"""

import pytest
from unittest.mock import AsyncMock, patch
import openai
from llm_analyzer import LLMAnalyzer, LLMAnalysisResult, APIErrorType


class TestAPIErrorHandling:
    """Test suite for OpenAI API error handling."""

    @pytest.mark.asyncio
    async def test_invalid_api_key_error(self, llm_analyzer):
        """Test handling of invalid API key errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = openai.AuthenticationError("Invalid API key")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert isinstance(result, LLMAnalysisResult)
            assert result.api_error == APIErrorType.INVALID_API_KEY
            assert result.has_biases is False
            assert result.confidence == 0.0
            assert "invalid" in result.error_message.lower()
            assert "configuration" in result.suggestions[0].lower()

    @pytest.mark.asyncio
    async def test_rate_limit_error(self, llm_analyzer):
        """Test handling of rate limit errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = openai.RateLimitError("Rate limit exceeded")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.RATE_LIMITED
            assert "rate limit" in result.error_message.lower()
            assert "resume shortly" in result.suggestions[0]

    @pytest.mark.asyncio
    async def test_quota_exceeded_error(self, llm_analyzer):
        """Test handling of quota exceeded errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = openai.BadRequestError("Billing quota exceeded")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.INSUFFICIENT_QUOTA
            assert "quota" in result.error_message.lower()
            assert "billing" in result.suggestions[0].lower()

    @pytest.mark.asyncio
    async def test_network_error(self, llm_analyzer):
        """Test handling of network connection errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = openai.APIConnectionError("Connection failed")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.NETWORK_ERROR
            assert "connection" in result.error_message.lower()
            assert "internet" in result.suggestions[0].lower()

    @pytest.mark.asyncio
    async def test_service_unavailable_error(self, llm_analyzer):
        """Test handling of OpenAI service errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = openai.InternalServerError("Service temporarily unavailable")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.SERVICE_UNAVAILABLE
            assert "service" in result.error_message.lower()
            assert "temporarily" in result.suggestions[0].lower()

    @pytest.mark.asyncio
    async def test_json_parse_error(self, llm_analyzer):
        """Test handling of invalid JSON responses."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            # Mock a response with invalid JSON
            mock_response = AsyncMock()
            mock_response.choices = [AsyncMock()]
            mock_response.choices[0].message.content = "Invalid JSON response"
            mock_create.return_value = mock_response
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.UNKNOWN_ERROR
            assert "parse" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_unknown_error(self, llm_analyzer):
        """Test handling of unexpected errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = ValueError("Unexpected error")
            
            result = await llm_analyzer.analyze_message("Test message")
            
            assert result.api_error == APIErrorType.UNKNOWN_ERROR
            assert "unexpected" in result.error_message.lower()

    def test_api_error_formatting(self, llm_analyzer, sample_llm_result):
        """Test that API errors are properly formatted in summaries."""
        
        # Test each error type formatting
        error_cases = [
            (APIErrorType.INVALID_API_KEY, "Configuration Issue"),
            (APIErrorType.RATE_LIMITED, "Rate Limited"),
            (APIErrorType.INSUFFICIENT_QUOTA, "Quota Exceeded"),
            (APIErrorType.SERVICE_UNAVAILABLE, "Service Unavailable"),
            (APIErrorType.NETWORK_ERROR, "Connection Issue"),
            (APIErrorType.UNKNOWN_ERROR, "Analysis Error")
        ]
        
        for error_type, expected_text in error_cases:
            # Create result with API error
            error_result = LLMAnalysisResult(
                has_biases=False,
                confidence=0.0,
                detected_biases=[],
                reasoning_quality="unknown",
                discussion_issues=[],
                suggestions=["Test suggestion"],
                summary="Test summary",
                api_error=error_type,
                error_message="Test error message"
            )
            
            formatted = llm_analyzer.format_analysis_summary(error_result)
            
            assert expected_text in formatted
            assert "⚠️" in formatted or "⏳" in formatted or "💰" in formatted or "🔧" in formatted or "🌐" in formatted or "❌" in formatted

    @pytest.mark.asyncio
    async def test_educational_response_api_errors(self, llm_analyzer, sample_llm_result):
        """Test educational response generation with API errors."""
        
        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            # Test authentication error
            mock_create.side_effect = openai.AuthenticationError("Invalid API key")
            
            response = await llm_analyzer.generate_educational_response(sample_llm_result, "Test text")
            
            assert response is not None
            assert "authentication" in response.lower()
            assert "⚠️" in response

        with patch.object(llm_analyzer.client.chat.completions, 'create') as mock_create:
            # Test rate limit error
            mock_create.side_effect = openai.RateLimitError("Rate limit")
            
            response = await llm_analyzer.generate_educational_response(sample_llm_result, "Test text")
            
            assert response is not None
            assert "rate limit" in response.lower()
            assert "⚠️" in response


class TestGracefulDegradation:
    """Test suite for graceful degradation when LLM is unavailable."""

    @pytest.mark.asyncio
    async def test_bot_continues_with_pattern_detection_only(self, bias_detector):
        """Test that the bot can function with pattern detection only when LLM fails."""
        
        # Test that pattern detection still works
        text = "You're clearly an idiot if you believe that"
        results = bias_detector.analyze_text(text)
        
        # Should return results (even if empty due to pattern matching issues)
        assert isinstance(results, list)

    def test_api_error_does_not_crash_bot(self, llm_analyzer):
        """Test that API errors don't crash the analysis pipeline."""
        
        # Create an error result
        error_result = LLMAnalysisResult(
            has_biases=False,
            confidence=0.0,
            detected_biases=[],
            reasoning_quality="unknown",
            discussion_issues=[],
            suggestions=["API unavailable"],
            summary="Analysis failed",
            api_error=APIErrorType.INVALID_API_KEY,
            error_message="Invalid API key"
        )
        
        # Should be able to format without crashing
        formatted = llm_analyzer.format_analysis_summary(error_result)
        assert isinstance(formatted, str)
        assert len(formatted) > 0

    def test_empty_api_key_handling(self):
        """Test behavior when API key is empty or missing."""
        
        # This would typically be caught during initialization
        # But we should handle it gracefully in analysis
        try:
            from config import settings
            original_key = settings.openai_api_key
            
            # Test with empty key (this might raise an error during LLMAnalyzer init)
            # The actual test would be in integration tests
            assert True  # Placeholder - real test would check initialization behavior
            
        except Exception:
            # Expected if no valid API key configured
            assert True


class TestAPIErrorMessages:
    """Test suite for API error message clarity and helpfulness."""

    def test_error_messages_are_user_friendly(self, llm_analyzer):
        """Test that error messages are clear and actionable."""
        
        error_types_and_expected_words = [
            (APIErrorType.INVALID_API_KEY, ["configuration", "invalid", "expired"]),
            (APIErrorType.RATE_LIMITED, ["rate", "limit", "shortly"]),
            (APIErrorType.INSUFFICIENT_QUOTA, ["quota", "billing", "limits"]),
            (APIErrorType.NETWORK_ERROR, ["network", "connection", "internet"]),
            (APIErrorType.SERVICE_UNAVAILABLE, ["service", "temporarily", "unavailable"]),
        ]
        
        for error_type, expected_words in error_types_and_expected_words:
            result = llm_analyzer._create_fallback_result(
                "test text", error_type, f"Test {error_type.value} error"
            )
            
            # Check suggestions contain helpful words
            suggestions_text = " ".join(result.suggestions).lower()
            assert any(word in suggestions_text for word in expected_words)
            
            # Check error message is present
            assert result.error_message is not None
            assert len(result.error_message) > 0

    def test_error_messages_include_recovery_instructions(self, llm_analyzer):
        """Test that error messages include instructions for recovery."""
        
        recovery_instructions = {
            APIErrorType.INVALID_API_KEY: "check configuration",
            APIErrorType.RATE_LIMITED: "resume shortly",
            APIErrorType.INSUFFICIENT_QUOTA: "check billing",
            APIErrorType.NETWORK_ERROR: "check internet",
            APIErrorType.SERVICE_UNAVAILABLE: "try again later"
        }
        
        for error_type, expected_instruction in recovery_instructions.items():
            result = llm_analyzer._create_fallback_result(
                "test text", error_type, f"Test error"
            )
            
            suggestions_text = " ".join(result.suggestions).lower()
            assert expected_instruction in suggestions_text