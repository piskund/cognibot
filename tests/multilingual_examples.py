#!/usr/bin/env python3
"""
Multilingual Examples for CogniBot Testing

This script demonstrates various bias examples in different languages 
to test the bot's multilingual analysis capabilities.
"""

import sys
from pathlib import Path

# Add src directory to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from bias_detector import BiasDetector


def test_multilingual_examples():
    """Test examples in different languages showing various biases."""
    
    # Test cases with biases in different languages
    test_cases = [
        {
            "language": "🇷🇺 Russian",
            "examples": [
                {
                    "text": "Ты явно идиот, если веришь в это",
                    "bias_type": "Ad Hominem",
                    "translation": "You're clearly an idiot if you believe this"
                },
                {
                    "text": "Все знают, что это правда",
                    "bias_type": "Bandwagon/Appeal to Popularity", 
                    "translation": "Everyone knows this is true"
                },
                {
                    "text": "Всякая селедка рыба, значит всякая рыба - селедка",
                    "bias_type": "Logical Fallacy (Affirming Consequent)",
                    "translation": "Every herring is a fish, therefore every fish is a herring"
                },
                {
                    "text": "Значит, ты говоришь, что мы должны просто сдаться?",
                    "bias_type": "Strawman Fallacy",
                    "translation": "So you're saying we should just give up?"
                }
            ]
        },
        {
            "language": "🇪🇸 Spanish", 
            "examples": [
                {
                    "text": "Eres claramente un idiota si crees eso",
                    "bias_type": "Ad Hominem",
                    "translation": "You're clearly an idiot if you believe that"
                },
                {
                    "text": "Todo el mundo sabe que esto es verdad",
                    "bias_type": "Bandwagon/Appeal to Popularity",
                    "translation": "Everyone knows this is true"
                },
                {
                    "text": "O estás con nosotros o contra nosotros",
                    "bias_type": "False Dichotomy",
                    "translation": "You're either with us or against us"
                }
            ]
        },
        {
            "language": "🇫🇷 French",
            "examples": [
                {
                    "text": "Tu es clairement un idiot si tu crois ça",
                    "bias_type": "Ad Hominem", 
                    "translation": "You're clearly an idiot if you believe that"
                },
                {
                    "text": "Tout le monde sait que c'est vrai",
                    "bias_type": "Bandwagon/Appeal to Popularity",
                    "translation": "Everyone knows this is true"
                },
                {
                    "text": "Alors tu dis qu'on devrait abandonner complètement?",
                    "bias_type": "Strawman Fallacy",
                    "translation": "So you're saying we should give up completely?"
                }
            ]
        },
        {
            "language": "🇩🇪 German",
            "examples": [
                {
                    "text": "Du bist offensichtlich ein Idiot, wenn du das glaubst",
                    "bias_type": "Ad Hominem",
                    "translation": "You're obviously an idiot if you believe that"
                },
                {
                    "text": "Jeder weiß, dass das wahr ist",
                    "bias_type": "Bandwagon/Appeal to Popularity", 
                    "translation": "Everyone knows this is true"
                }
            ]
        }
    ]
    
    print("🌍 CogniBot Multilingual Bias Examples")
    print("=" * 60)
    print("These examples show cognitive biases in different languages.")
    print("The LLM should analyze AND respond in the same language as input.\n")
    
    for language_group in test_cases:
        print(f"{language_group['language']}")
        print("-" * 40)
        
        for i, example in enumerate(language_group['examples'], 1):
            print(f"\n{i}. **{example['bias_type']}**")
            print(f"   Text: {example['text']}")
            print(f"   Translation: {example['translation']}")
            
            # Test with pattern detection (won't catch non-English)
            detector = BiasDetector()
            results = detector.analyze_text(example['text'])
            if results:
                print(f"   Pattern Detection: ✅ {len(results)} patterns found")
                for result in results:
                    print(f"      • {result.bias_type.value} ({result.confidence:.0%})")
            else:
                print(f"   Pattern Detection: ❌ No patterns (expected for non-English)")
        
        print("\n")

    print("🧪 **Testing Instructions:**")
    print("""
1. **With Valid API Key:**
   ```bash
   # Set your OpenAI API key
   export OPENAI_API_KEY="your_key_here"
   
   # Test Russian analysis
   python tests/run_russian_test.py
   
   # Run multilingual tests  
   pytest tests/test_multilingual_advanced.py -v
   ```

2. **Expected Behavior:**
   • Russian input → Russian analysis response
   • Spanish input → Spanish analysis response  
   • French input → French analysis response
   • Pattern detection works mainly for English
   • LLM analysis should work for all languages

3. **Key Test Points:**
   • ✅ LLM understands biases in multiple languages
   • ✅ LLM responds in the same language as input
   • ✅ Error handling works regardless of language
   • ✅ Bot gracefully degrades when API unavailable
    """)


if __name__ == "__main__":
    test_multilingual_examples()