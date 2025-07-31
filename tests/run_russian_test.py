#!/usr/bin/env python3
"""
Simple runner for the Russian logical fallacy test.
This provides a quick way to test the specific Russian sentence.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from bias_detector import BiasDetector
from llm_analyzer import LLMAnalyzer


async def test_russian_sentence():
    """Test the Russian logical fallacy sentence."""
    
    # The Russian sentence (logical fallacy: affirming the consequent)
    russian_text = "Всякая селедка рыба, значит всякая рыба - селедка"
    
    print("🧠 Testing Russian Multilingual Analysis")
    print("="*60)
    print(f"📝 Russian Text: {russian_text}")
    print(f"🎯 Testing: LLM should analyze AND respond in Russian")
    print(f"⚠️  Expected: Logical fallacy detection in Russian")
    print("\n" + "="*60)
    
    # Test 1: Pattern-based detection
    print("\n1️⃣ Pattern-based Bias Detection:")
    print("-" * 40)
    
    detector = BiasDetector()
    pattern_results = detector.analyze_text(russian_text)
    
    if pattern_results:
        print("✅ Detected patterns:")
        for result in pattern_results:
            bias_name = result.bias_type.value.replace('_', ' ').title()
            print(f"   • {bias_name} (confidence: {result.confidence:.0%})")
    else:
        print("❌ No patterns detected (expected - this is a logical structure issue)")
    
    # Test 2: LLM Analysis
    print("\n2️⃣ LLM Analysis:")
    print("-" * 40)
    
    try:
        analyzer = LLMAnalyzer()
        print("⏳ Calling OpenAI API...")
        
        llm_result = await analyzer.analyze_message(russian_text)
        
        print(f"✅ Analysis Results:")
        print(f"   Has biases: {llm_result.has_biases}")
        print(f"   Confidence: {llm_result.confidence:.0%}")
        print(f"   Detected biases: {', '.join(llm_result.detected_biases)}")
        print(f"   Reasoning quality: {llm_result.reasoning_quality}")
        print(f"   Summary: {llm_result.summary}")
        
        # Check if response is in Russian (contains Cyrillic characters)
        has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in llm_result.summary)
        print(f"   🌍 Response in Russian: {'✅ Yes' if has_cyrillic else '❌ No (English detected)'}")
        
        # Test the formatted response (what users would see)
        print(f"\n📋 Bot Response Preview:")
        print("-" * 40)
        formatted = analyzer.format_analysis_summary(llm_result)
        print(formatted)
        
    except Exception as e:
        print(f"❌ LLM Analysis failed: {e}")
        print("💡 Make sure your OpenAI API key is set correctly in .env file")
    
    print("\n" + "="*60)
    print("✅ Russian sentence test completed!")


if __name__ == "__main__":
    asyncio.run(test_russian_sentence())