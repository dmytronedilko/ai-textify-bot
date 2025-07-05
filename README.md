# 🎙️ Telegram Textify Bot

A Telegram bot that converts voice messages and video notes to text using OpenAI Whisper API. Built with aiogram and Docker.

## 🚀 Features

- **Voice Message Recognition** — converts Telegram voice messages to text
- **Video Notes Processing** — extracts audio from circular video messages and transcribes
- **Multi-language Support** — recognizes speech in multiple languages
- **Fast Processing** — typically 3-6 seconds for standard messages
- **OpenAI Whisper Integration** — uses OpenAI's speech recognition API
- **Docker Ready** — fully containerized application

## 🛠️ Technology Stack

- **aiogram 3.x** — modern async Telegram Bot framework
- **OpenAI Whisper API** — speech recognition service
- **Docker** — containerization
- **Python 3.13** — backend language

## 🤖 Bot Commands

- `/start` — start the bot
- `/textify` — converts voice and video messages to text (only in groups) 

## 📊 Performance

- **Processing Speed** — 2-5 seconds for voice messages, 3-8 seconds for video notes
- **File Size Limit** — up to 25MB
- **Languages** — Transcribe audio into whatever language the audio is in.

## 🔒 Security

- Audio files are processed and immediately deleted