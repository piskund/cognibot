# CogniBot Test Suite

This directory contains comprehensive tests for the CogniBot cognitive bias detection system.

## Test Structure

```
tests/
├── __init__.py                 # Package initialization
├── conftest.py                # Shared pytest fixtures and configuration
├── pytest.ini                # Pytest configuration
├── README.md                  # This file
├── test_bias_detector.py      # Unit tests for pattern-based bias detection
├── test_llm_analyzer.py       # Unit tests for LLM-based analysis
├── test_multilingual.py       # Tests for multilingual support (including Russian test)
├── test_integration.py        # Integration tests for component interaction
├── test_legacy.py             # Legacy test script (migrated from src/)
└── run_russian_test.py        # Quick runner for Russian logical fallacy test
```

## Running Tests

### Prerequisites

```bash
# Install testing dependencies
pip install pytest pytest-asyncio

# Set up your .env file with OpenAI API key (for LLM tests)
cp src/env_template.txt .env
# Edit .env and add your OPENAI_API_KEY
```

### Test Commands

```bash
# Run all tests
pytest

# Run only unit tests (fast, no API calls)
pytest -m "not integration and not slow"

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_bias_detector.py

# Run the Russian logical fallacy test
pytest tests/test_multilingual.py::TestMultilingualSupport::test_russian_logical_fallacy -v

# Run legacy test script (direct execution)
python tests/test_legacy.py

# Quick Russian test runner
python tests/run_russian_test.py
```

## Test Categories

### 🧪 Unit Tests
- **test_bias_detector.py**: Tests pattern-based bias detection
- **test_llm_analyzer.py**: Tests LLM analysis functionality
- Fast execution, no external dependencies

### 🌐 Integration Tests  
- **test_integration.py**: Tests component interaction
- **test_multilingual.py**: Tests multilingual support including Russian
- Requires OpenAI API key for LLM analysis

### 📊 Test Markers

- `@pytest.mark.unit`: Fast unit tests
- `@pytest.mark.integration`: Tests requiring external services (OpenAI API)
- `@pytest.mark.slow`: Longer-running tests
- `@pytest.mark.asyncio`: Async tests (required for LLM analysis)

## Key Test Cases

### Russian Logical Fallacy
```
Text: "Всякая селедка рыба, значит всякая рыба - селедка"
Translation: "Every herring is a fish, therefore every fish is a herring"
Expected: Logical fallacy (affirming the consequent)
```

### English Bias Examples
- **Ad Hominem**: "You're clearly an idiot if you believe that"
- **Bandwagon**: "Everyone knows this is true"
- **False Dichotomy**: "You're either with us or against us"
- **Strawman**: "So you're saying we should just give up completely?"

## Configuration

Tests use `conftest.py` for shared fixtures and `pytest.ini` for configuration:

- Automatic test discovery
- Async test support
- Warning filters
- Test markers for categorization

## CI/CD Ready

This test structure is ready for continuous integration:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install pytest pytest-asyncio
    pytest -m "not integration"  # Skip API-dependent tests in CI
```

## Development Workflow

1. **Write tests first** (TDD approach)
2. **Run unit tests frequently** during development
3. **Run integration tests** before commits
4. **Use markers** to control which tests run in different environments

## Notes

- Tests requiring OpenAI API will be skipped if no API key is provided
- Pattern-based tests run without external dependencies
- Fixtures in `conftest.py` provide reusable test data and mocks