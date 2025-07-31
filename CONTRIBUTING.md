# Contributing to CogniBot

Thank you for your interest in contributing to CogniBot! This project aims to improve online discourse through cognitive bias detection and is developed for non-commercial, educational purposes.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `python test_analysis.py`
6. Submit a pull request

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Keep functions focused and concise

### Adding New Bias Detection

To add new cognitive bias patterns:

1. **Update `BiasType` enum** in `bias_detector.py`:
```python
NEW_BIAS_NAME = "new_bias_name"
```

2. **Add detection patterns** in `_initialize_patterns()`:
```python
BiasType.NEW_BIAS_NAME: [
    r"regex_pattern_1",
    r"regex_pattern_2",
],
```

3. **Add description** in `_initialize_descriptions()`:
```python
BiasType.NEW_BIAS_NAME: "Clear description of the bias",
```

4. **Add test cases** in `test_analysis.py`

### LLM Prompt Improvements

When improving the LLM analysis prompts:
- Focus on educational value
- Maintain constructive tone
- Test with various message types
- Consider cultural sensitivity

## Copyright and Licensing

### Copyright Headers
All new code files should include the copyright header:

```python
"""
File description

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""
```

### Contributions
By contributing to this project, you agree that your contributions will be licensed under the same MIT License. You retain copyright to your contributions while granting the project maintainer the right to use them under the MIT License.

### Attribution
Significant contributions may be acknowledged in the README or changelog. Please include your name and email (if you wish) in your pull request description.

## Non-Commercial Purpose

This project is developed for educational and community improvement purposes. Contributions should align with this non-commercial, educational mission.

## Contact

For questions about contributing, contact:
**Dmytro Piskun** - [dmytro.piskun@gmail.com](mailto:dmytro.piskun@gmail.com)

## Code of Conduct

- Be respectful and constructive in discussions
- Focus on improving discourse quality
- Avoid implementing features that could be used for harassment
- Consider the educational impact of your contributions
- Test thoroughly before submitting

Thank you for helping make online discussions more thoughtful and productive! 