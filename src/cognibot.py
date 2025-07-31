#!/usr/bin/env python3
"""
CogniBot - Telegram Bot for Cognitive Bias Detection
Monitors Telegram channels and analyzes messages for cognitive biases and logical errors.

Copyright (c) 2025 Dmytro Piskun <dmytro.piskun@gmail.com>

This project is licensed under the MIT License - see the LICENSE file for details.
"""

import asyncio
import time
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta

from telegram import Update, Message
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from telegram.error import TelegramError
from loguru import logger
import sys

from config import settings
from bias_detector import BiasDetector, BiasAnalysis
from llm_analyzer import LLMAnalyzer, LLMAnalysisResult

class CogniBot:
    """Main bot class for cognitive bias detection."""
    
    def __init__(self):
        self.bias_detector = BiasDetector()
        self.llm_analyzer = LLMAnalyzer()
        self.processed_messages: Set[int] = set()
        self.last_analysis_time: Dict[int, datetime] = {}
        self.application = None
        
        # Setup logging
        logger.remove()
        logger.add(sys.stderr, format="{time} | {level} | {message}", level="INFO")
        logger.add("cognibot.log", rotation="1 MB", level="DEBUG")
    
    async def initialize_bot(self):
        """Initialize the Telegram bot application."""
        self.application = Application.builder().token(settings.telegram_bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Add message handler for channel monitoring
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_message
        ))
        
        logger.info("Bot initialized successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
🧠 **Welcome to CogniBot!**

I analyze messages for cognitive biases and logical errors to help improve discussion quality.

**Commands:**
• `/help` - Show this help message
• `/analyze [text]` - Analyze specific text
• `/stats` - Show analysis statistics

**Features:**
• Monitors channel messages automatically
• Detects cognitive biases and logical fallacies
• Provides educational feedback
• Helps improve critical thinking

I'm here to foster better discourse, not to criticize!
        """
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
🧠 **CogniBot Help**

**What I detect:**
• Cognitive biases (confirmation bias, anchoring, etc.)
• Logical fallacies (ad hominem, strawman, false dichotomy)
• Discussion quality issues
• Reasoning errors

**How I work:**
1. Monitor channel messages
2. Analyze using pattern matching + AI
3. Provide constructive feedback when issues found

**Commands:**
• `/analyze <text>` - Manually analyze text
• `/stats` - Show bot statistics

**Note:** I only respond when significant issues are detected to avoid spam.
        """
        await update.message.reply_text(help_text)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command for manual analysis."""
        if not context.args:
            await update.message.reply_text("Please provide text to analyze: `/analyze Your text here`")
            return
        
        text_to_analyze = " ".join(context.args)
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Perform analysis
            pattern_results = self.bias_detector.analyze_text(text_to_analyze)
            llm_result = await self.llm_analyzer.analyze_message(text_to_analyze)
            
            # Format response
            response = await self._format_analysis_response(pattern_results, llm_result, manual=True)
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in manual analysis: {e}")
            await update.message.reply_text("Sorry, analysis failed. Please try again later.")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        stats_text = f"""
📊 **CogniBot Statistics**

• **Messages processed:** {len(self.processed_messages)}
• **Active since:** Bot startup
• **Analysis threshold:** {settings.analysis_threshold}
• **Channel monitoring:** {settings.telegram_channel_id}

**Bias Detection:**
• Pattern-based detection active
• LLM analysis with {settings.openai_model}
• Educational response generation
        """
        await update.message.reply_text(stats_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages from monitored channels."""
        message = update.message
        
        # Skip if no message or no text
        if not message or not message.text:
            return
        
        # Skip if message already processed
        if message.message_id in self.processed_messages:
            return
        
        # Debug: Log channel info
        logger.info(f"Message from chat ID: {message.chat.id}, chat title: {message.chat.title}, chat username: {getattr(message.chat, 'username', None)}")
        
        # Skip if not from monitored channel(s) (if specified)
        if settings.telegram_channel_id or settings.telegram_channels:
            # Get list of monitored channels
            monitored_channels = []
            if settings.telegram_channel_id:
                monitored_channels.append(settings.telegram_channel_id.replace('@', ''))
            if settings.telegram_channels:
                additional_channels = [ch.strip().replace('@', '') for ch in settings.telegram_channels.split(',') if ch.strip()]
                monitored_channels.extend(additional_channels)
            
            chat_id_str = str(message.chat.id)
            chat_username = getattr(message.chat, 'username', None)
            
            # Check if message is from any monitored channel (by ID or username)
            is_monitored_channel = any(
                chat_id_str == channel or chat_username == channel
                for channel in monitored_channels
            )
            
            if not is_monitored_channel:
                logger.info(f"Skipping message - not from monitored channels. Expected: {monitored_channels}, Got chat ID: {message.chat.id}, username: {chat_username}")
                return
        
        # Skip very short messages
        if len(message.text) < 50:
            return
        
        # Rate limiting check
        if await self._is_rate_limited(message.chat.id):
            return
        
        try:
            await self._analyze_and_respond(message)
            
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")
        
        finally:
            self.processed_messages.add(message.message_id)
    
    async def _analyze_and_respond(self, message: Message):
        """Analyze a message and respond if significant issues found."""
        text = message.text
        
        logger.info(f"Analyzing message from {message.from_user.username}: {text[:100]}...")
        
        # Run both analyses
        pattern_results = self.bias_detector.analyze_text(text)
        llm_result = await self.llm_analyzer.analyze_message(text)
        
        # Determine if response is warranted
        should_respond = await self._should_respond(pattern_results, llm_result)
        
        if should_respond:
            # Format response
            response = await self._format_analysis_response(pattern_results, llm_result)
            
            # Send response as reply
            await message.reply_text(response, parse_mode='Markdown')
            
            # Update rate limiting
            self.last_analysis_time[message.chat.id] = datetime.now()
            
            logger.info(f"Sent analysis response for message {message.message_id}")
        else:
            logger.debug(f"No significant issues found in message {message.message_id}")
    
    async def _should_respond(self, pattern_results: List[BiasAnalysis], llm_result: LLMAnalysisResult) -> bool:
        """Determine if the bot should respond based on analysis results."""
        # Check pattern-based results
        high_confidence_patterns = [r for r in pattern_results if r.confidence > settings.analysis_threshold]
        
        # Check LLM results
        llm_significant = llm_result.confidence > settings.analysis_threshold and llm_result.has_biases
        
        return len(high_confidence_patterns) > 0 or llm_significant
    
    async def _format_analysis_response(self, pattern_results: List[BiasAnalysis], 
                                      llm_result: LLMAnalysisResult, manual: bool = False) -> str:
        """Format the analysis results into a response message."""
        response_parts = []
        
        if manual:
            response_parts.append("🔍 **Manual Analysis Results:**\n")
        else:
            response_parts.append("🧠 **Cognitive Bias Analysis:**\n")
        
        # Add LLM analysis summary
        llm_summary = self.llm_analyzer.format_analysis_summary(llm_result)
        response_parts.append(llm_summary)
        
        # Add pattern-based results if significant
        if pattern_results:
            high_confidence = [r for r in pattern_results if r.confidence > 0.6]
            if high_confidence:
                response_parts.append("\n🔍 **Additional Patterns Detected:**")
                for result in high_confidence[:3]:  # Limit to 3 results
                    bias_name = result.bias_type.value.replace('_', ' ').title()
                    response_parts.append(f"• {bias_name} ({result.confidence:.0%})")
        
        # Add educational note
        if not manual:
            response_parts.append("\n💡 *This analysis aims to improve discussion quality, not to criticize. Consider this feedback constructively.*")
        
        return "\n".join(response_parts)
    
    async def _is_rate_limited(self, chat_id: int) -> bool:
        """Check if responses to this chat are rate limited."""
        if chat_id not in self.last_analysis_time:
            return False
        
        time_since_last = datetime.now() - self.last_analysis_time[chat_id]
        return time_since_last < timedelta(minutes=settings.response_delay)
    
    async def run(self):
        """Run the bot."""
        logger.info("Starting CogniBot...")
        
        await self.initialize_bot()
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info(f"Bot is running and monitoring channel: {settings.telegram_channel_id}")
        
        try:
            # Keep the bot running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

async def main():
    """Main entry point."""
    bot = CogniBot()
    await bot.run()

if __name__ == "__main__":
    # Check configuration
    try:
        # Validate settings
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        # Run the bot
        asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1) 