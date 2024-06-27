# AI News Aggregator

This repository contains an automated system for aggregating and filtering AI-related news from various sources. It's designed to keep communication and marketing professionals up-to-date with the latest developments in artificial intelligence.

## Features

- Automatically fetches AI news from multiple sources
- Filters content based on relevance to AI and related topics
- Updates regularly using GitHub Actions
- Saves aggregated news in an easily readable format

## How It Works

1. The script `ai_news_scanner.py` runs on a scheduled basis (every 12 hours by default).
2. It fetches news from predefined sources using RSS feeds and web scraping.
3. The content is filtered for relevance using a set of AI-related keywords.
4. Relevant news items are saved to `ai_news_updates.txt`.
5. The updated file is committed and pushed to the repository.

## Sources

Currently, the aggregator pulls from the following sources:

- TechCrunch (AI category)
- The Verge (AI category)
- Wired (AI category)
- NVIDIA Blog
- OpenAI Blog

More sources can be added by modifying the `sources` list in `ai_news_scanner.py`.

## Keywords

The script filters content based on the following keywords:

- artificial intelligence
- AI
- machine learning
- deep learning
- neural network
- AI ethics
- AI legislation
- AI regulation
- AI risk
- AI safety

You can modify these keywords in the `keywords` list in `ai_news_scanner.py`.

## Setup

To set up this project locally:

1. Clone the repository:
