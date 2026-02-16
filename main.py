"""
News Summarizer Telegram Bot
Author: [Apna Naam]
Registration: [Apna Registration No.]
"""

import asyncio
import sys
import os
import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# 🔥 CRITICAL FIX: Event loop for Python compatibility
if sys.platform == "win32" and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Create event loop agar nahi hai
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# ==================== CONFIGURATION ====================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "demo")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== NEWS SOURCES ====================
NEWS_SOURCES = {
    "india": {
        "name": "🇮🇳 India News",
        "url": f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    },
    "technology": {
        "name": "💻 Technology",
        "url": f"https://newsapi.org/v2/top-headlines?category=technology&country=in&apiKey={NEWS_API_KEY}"
    },
    "business": {
        "name": "📈 Business",
        "url": f"https://newsapi.org/v2/top-headlines?category=business&country=in&apiKey={NEWS_API_KEY}"
    },
    "science": {
        "name": "🔬 Science",
        "url": f"https://newsapi.org/v2/top-headlines?category=science&country=in&apiKey={NEWS_API_KEY}"
    }
}

# ==================== DEMO NEWS DATA ====================
DEMO_NEWS = {
    "india": [
        {"title": "India launches Chandrayaan-4 mission to Moon", "source": "ISRO", "description": "ISRO successfully launches next lunar mission...", "url": "#"},
        {"title": "New education policy implemented across all states", "source": "Education Ministry", "description": "Major reforms in school education...", "url": "#"},
        {"title": "Stock market reaches all-time high of 85,000", "source": "BSE", "description": "Sensex crosses 85,000 mark for first time...", "url": "#"}
    ],
    "technology": [
        {"title": "WhatsApp introduces new privacy features", "source": "TechCrunch", "description": "New features include disappearing messages...", "url": "#"},
        {"title": "Google unveils Gemini AI model in India", "source": "The Verge", "description": "Advanced AI model now available in Indian languages...", "url": "#"},
        {"title": "iPhone 16 launch date announced", "source": "Apple Insider", "description": "Apple confirms September event for new iPhone...", "url": "#"}
    ],
    "business": [
        {"title": "Reliance acquires major retail chain", "source": "Economic Times", "description": "Deal worth ₹5000 crore signed...", "url": "#"},
        {"title": "RBI keeps repo rate unchanged", "source": "Bloomberg", "description": "Central bank maintains status quo...", "url": "#"},
        {"title": "Startup funding reaches ₹1 lakh crore", "source": "Business Standard", "description": "Indian startups see record funding in Q1...", "url": "#"}
    ],
    "science": [
        {"title": "ISRO successfully tests crew escape system", "source": "ISRO", "description": "Critical test for Gaganyaan mission successful...", "url": "#"},
        {"title": "New malaria vaccine developed by Indian scientists", "source": "ICMR", "description": "Breakthrough in vaccine research...", "url": "#"},
        {"title": "Quantum computing breakthrough at IIT Bombay", "source": "Nature India", "description": "Researchers achieve 100-qubit milestone...", "url": "#"}
    ]
}

# ==================== COMMAND HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with inline keyboard"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("📰 Latest News", callback_data="news_india")],
        [InlineKeyboardButton("💻 Technology", callback_data="news_technology"),
         InlineKeyboardButton("📈 Business", callback_data="news_business")],
        [InlineKeyboardButton("🔬 Science", callback_data="news_science"),
         InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"👋 **Namaste {user.first_name}!**\n\n"
        f"🤖 Main **News Summarizer Bot** hoon.\n"
        f"📰 Latest news summaries with AI summarization.\n\n"
        f"**Features:**\n"
        f"• 🇮🇳 India news\n"
        f"• 💻 Technology\n"
        f"• 📈 Business\n"
        f"• 🔬 Science\n\n"
        f"**Commands:**\n"
        f"/news - Get news summaries\n"
        f"/help - Show help\n"
        f"/about - About this bot"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /news command - show category selection"""
    keyboard = [
        [InlineKeyboardButton("🇮🇳 India News", callback_data="news_india")],
        [InlineKeyboardButton("💻 Technology", callback_data="news_technology"),
         InlineKeyboardButton("📈 Business", callback_data="news_business")],
        [InlineKeyboardButton("🔬 Science", callback_data="news_science"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📰 **Select News Category:**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message"""
    help_text = (
        "📚 **How to Use This Bot**\n\n"
        "**Commands:**\n"
        "• /start - Start the bot\n"
        "• /news - Get news summaries\n"
        "• /help - Show this help\n"
        "• /about - About the bot\n\n"
        "**Categories:**\n"
        "• India News 🇮🇳\n"
        "• Technology 💻\n"
        "• Business 📈\n"
        "• Science 🔬\n\n"
        "**Developer:** [Apna Naam]\n"
        "**Registration:** [Apna Registration No.]"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot"""
    about_text = (
        "🤖 **About News Summarizer Bot**\n\n"
        "**Version:** 1.0.0\n"
        "**Developer:** [Apna Naam]\n"
        "**Registration:** [Apna Registration No.]\n"
        "**Built with:** Python + python-telegram-bot\n"
        "**Hosted on:** Render (Free Tier)\n\n"
        "**Purpose:**\n"
        "This bot fetches latest news from various sources and provides concise summaries.\n\n"
        "**Data Sources:**\n"
        "• NewsAPI.org\n"
        "• Demo data (when API key not available)\n\n"
        "**Contact:**\n"
        "• Telegram: @your_username\n"
        "• GitHub: github.com/yourusername"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await help_command(update, context)
        return
    
    if query.data == "cancel":
        await query.edit_message_text("❌ Cancelled. Send /start to begin again.")
        return
    
    if query.data.startswith("news_"):
        category = query.data.replace("news_", "")
        await fetch_and_send_news(query, category)

async def fetch_and_send_news(query, category):
    """Fetch news for selected category and send to user"""
    await query.edit_message_text(f"🔍 Fetching {NEWS_SOURCES[category]['name']}...")
    
    try:
        news_items = await fetch_news_from_api(category)
        
        if not news_items:
            news_items = DEMO_NEWS.get(category, DEMO_NEWS["india"])
        
        summary = await generate_summary(news_items, category)
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"news_{category}"),
             InlineKeyboardButton("🔙 Categories", callback_data="back_to_categories")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            summary,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logger.error(f"Error in fetch_and_send_news: {e}")
        await query.edit_message_text(
            "❌ Error fetching news. Please try again later.\n\n"
            "Send /start to continue."
        )

async def fetch_news_from_api(category):
    """Fetch real news from NewsAPI"""
    if NEWS_API_KEY == "demo" or not NEWS_API_KEY:
        return None
    
    try:
        url = NEWS_SOURCES[category]["url"]
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            if articles:
                formatted_articles = []
                for article in articles[:5]:
                    formatted_articles.append({
                        'title': article.get('title', 'No title'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'description': article.get('description', 'No description available'),
                        'url': article.get('url', '#'),
                        'published': article.get('publishedAt', '')[:10]
                    })
                return formatted_articles
    except Exception as e:
        logger.error(f"API fetch error: {e}")
    
    return None

async def generate_summary(news_items, category):
    """Generate a formatted summary from news items"""
    category_names = {
        "india": "🇮🇳 India News",
        "technology": "💻 Technology News",
        "business": "📈 Business News",
        "science": "🔬 Science News"
    }
    
    cat_name = category_names.get(category, "📰 News")
    current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
    
    summary = f"**{cat_name}**\n"
    summary += f"📅 *{current_time}*\n\n"
    
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title', 'No title')
        source = item.get('source', 'Unknown')
        description = item.get('description', '')
        url = item.get('url', '')
        
        if ' - ' in title:
            title = title.split(' - ')[0]
        
        summary += f"**{i}. {title}**\n"
        summary += f"📌 *Source:* {source}\n"
        
        if description and description != "No description available":
            short_desc = description[:100] + "..." if len(description) > 100 else description
            summary += f"📝 {short_desc}\n"
        
        if url and url != '#':
            display_url = url.replace('https://', '').replace('http://', '')[:30]
            summary += f"🔗 [{display_url}]({url})\n"
        
        summary += "\n"
    
    summary += "---\n"
    summary += "🔹 _Powered by News Summarizer Bot_\n"
    summary += "🔄 Send /news for more categories"
    
    return summary

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to category selection"""
    keyboard = [
        [InlineKeyboardButton("🇮🇳 India News", callback_data="news_india")],
        [InlineKeyboardButton("💻 Technology", callback_data="news_technology"),
         InlineKeyboardButton("📈 Business", callback_data="news_business")],
        [InlineKeyboardButton("🔬 Science", callback_data="news_science")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        "📰 **Select News Category:**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ==================== MAIN FUNCTION ====================
def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Add callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("🤖 Bot started! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()