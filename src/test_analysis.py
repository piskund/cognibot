#!/usr/bin/env python3
"""
Test script for CogniBot analysis functions.
Run this to verify the bias detection and LLM analysis are working correctly.

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

import asyncio
from bias_detector import BiasDetector
from llm_analyzer import LLMAnalyzer

# Test messages with known biases
TEST_MESSAGES = [
    {
        "text": "You're clearly an idiot if you believe that. Only a moron would think otherwise.",
        "expected_biases": ["ad_hominem"]
    },
    {
        "text": "So you're saying we should just give up completely? That's not what I meant at all.",
        "expected_biases": ["strawman"]
    },
    {
        "text": "Everyone knows this is true. Most people agree with this statement.",
        "expected_biases": ["bandwagon"]
    },
    {
        "text": "You're either with us or against us. There's no middle ground on this issue.",
        "expected_biases": ["false_dichotomy"]
    },
    {
        "text": "This is a well-reasoned argument with good evidence and respectful tone.",
        "expected_biases": []
    }
]

async def test_bias_detection():
    """Test the bias detection functionality."""
    print("🧠 Testing Bias Detection\n" + "="*50)
    
    detector = BiasDetector()
    
    for i, test_case in enumerate(TEST_MESSAGES, 1):
        print(f"\nTest {i}: {test_case['text'][:60]}...")
        
        results = detector.analyze_text(test_case["text"])
        
        if results:
            print(f"✅ Detected biases:")
            for result in results:
                print(f"   • {result.bias_type.value} (confidence: {result.confidence:.0%})")
        else:
            print("❌ No biases detected")
        
        expected = test_case["expected_biases"]
        if expected:
            print(f"📝 Expected: {', '.join(expected)}")

async def test_llm_analysis():
    """Test the LLM analysis functionality."""
    print("\n\n🤖 Testing LLM Analysis\n" + "="*50)
    
    try:
        analyzer = LLMAnalyzer()
        
        # Test with a clearly biased message
        test_text = "You're an idiot if you believe that climate change is real. Everyone I know thinks it's fake."
        
        print(f"Analyzing: {test_text}")
        print("⏳ Calling OpenAI API...")
        
        result = await analyzer.analyze_message(test_text)
        
        print(f"\n✅ Analysis Results:")
        print(f"   Has biases: {result.has_biases}")
        print(f"   Confidence: {result.confidence:.0%}")
        print(f"   Detected biases: {', '.join(result.detected_biases)}")
        print(f"   Reasoning quality: {result.reasoning_quality}")
        print(f"   Summary: {result.summary}")
        
        # Test formatting
        formatted = analyzer.format_analysis_summary(result)
        print(f"\n📋 Formatted Summary:\n{formatted}")
        
    except Exception as e:
        print(f"❌ LLM Analysis failed: {e}")
        print("💡 Make sure your OpenAI API key is set correctly in .env file")

async def main():
    """Run all tests."""
    print("🚀 CogniBot Analysis Tests\n")
    
    await test_bias_detection()
    await test_llm_analysis()
    
    print("\n" + "="*50)
    print("✅ Tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 