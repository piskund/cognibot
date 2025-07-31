# CogniBot 🧠

A Telegram bot that analyzes messages for cognitive biases, logical fallacies, and discussion quality issues using AI. Designed to foster better discourse and critical thinking in online conversations.

## Features

- **Cognitive Bias Detection**: Identifies confirmation bias, anchoring bias, availability heuristic, and more
- **Logical Fallacy Recognition**: Detects ad hominem, strawman arguments, false dichotomies, etc.
- **Discussion Quality Analysis**: Evaluates reasoning patterns and communication style
- **Educational Responses**: Provides constructive feedback to improve discourse
- **Channel Monitoring**: Automatically analyzes messages in configured channels
- **Manual Analysis**: Use `/analyze` command for immediate text analysis

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cognibot
cd cognibot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the environment template:
```bash
cp env_template.txt .env
```

2. Edit `.env` with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username_or_id
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

### 4. Run the Bot

```bash
python cognibot.py
```

## Getting Bot Credentials

### Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Save the token provided

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Ensure you have sufficient credits

### Channel Setup

1. Add your bot to the desired channel as an admin
2. Get the channel ID/username:
   - For public channels: Use `@channelname`
   - For private channels: Use the numeric chat ID

## Usage

### Bot Commands

- `/start` - Welcome message and overview
- `/help` - Detailed help information
- `/analyze <text>` - Manually analyze provided text
- `/stats` - Show bot statistics

### Example Analysis

```
🧠 Cognitive Bias Analysis:

🟡 Cognitive Bias Analysis (Confidence: 75%)

🧠 Detected Issues:
• Confirmation bias
• Ad hominem attack

⚠️ Reasoning Quality: Fair

⚠️ Discussion Issues:
• Personal attacks instead of addressing arguments
• Selective evidence presentation

💡 Suggestions:
• Focus on the argument rather than the person
• Consider alternative perspectives
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Required |
| `TELEGRAM_CHANNEL_ID` | Channel to monitor | Required |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | gpt-4-turbo-preview |
| `ANALYSIS_THRESHOLD` | Confidence threshold for responses | 0.7 |
| `MAX_MESSAGE_LENGTH` | Maximum message length to analyze | 4000 |
| `RESPONSE_DELAY` | Minutes between responses in same chat | 2 |

## Detected Biases and Fallacies

### Cognitive Biases
- Confirmation Bias
- Anchoring Bias
- Availability Heuristic
- Survivorship Bias

### Logical Fallacies
- Ad Hominem
- Strawman Arguments
- False Dichotomy
- Appeal to Authority
- Bandwagon Fallacy
- Slippery Slope
- Circular Reasoning
- Hasty Generalization

### Discussion Issues
- Hostile communication patterns
- Poor evidence usage
- Lack of logical structure
- Closed-minded discourse

## Architecture

```
cognibot.py          # Main bot logic and Telegram integration
├── bias_detector.py # Pattern-based bias detection
├── llm_analyzer.py  # AI-powered analysis using OpenAI
├── config.py        # Configuration management
└── requirements.txt # Python dependencies
```

## Contributing

We welcome contributions to improve CogniBot! This project is developed for non-commercial, educational purposes.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Code style and development workflow
- Adding new bias detection patterns
- Improving LLM prompts
- Copyright and licensing requirements

**Quick start for contributors:**
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

For questions: [dmytro.piskun@gmail.com](mailto:dmytro.piskun@gmail.com)

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check bot token is correct
- Ensure bot is added to channel as admin
- Verify channel ID is correct

**Analysis not working:**
- Check OpenAI API key and credits
- Verify internet connectivity
- Check logs in `cognibot.log`

**Rate limiting:**
- Bot waits 2 minutes between responses by default
- Adjust `RESPONSE_DELAY` if needed

### Logs

Check `cognibot.log` for detailed error information:
```bash
tail -f cognibot.log
```

## Privacy and Ethics

- The bot only analyzes public channel messages
- No personal data is stored permanently
- Analysis is educational, not judgmental
- Designed to improve discourse quality
- Respects user privacy and Telegram ToS

## Author

**Dmytro Piskun**  
📧 Contact: [dmytro.piskun@gmail.com](mailto:dmytro.piskun@gmail.com)

This project is developed for non-commercial purposes to foster better discourse and critical thinking in online communities.

## License

MIT License - Copyright (c) 2025 Dmytro Piskun

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

See the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is designed for educational purposes to improve critical thinking and discourse quality. It should not be used to harass or criticize individuals. The analysis is based on patterns and AI interpretation, which may not always be accurate.

**Non-Commercial Use**: This project is intended for educational and community improvement purposes, not for commercial exploitation. 