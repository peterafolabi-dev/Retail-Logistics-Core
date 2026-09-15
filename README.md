# 🛒 RedCart — Retail-Logistics-Core

A full production e-commerce platform built solo with **Django**, featuring a Groq-powered AI shopping assistant, real payment processing, and fraud-aware review moderation.

**Live at:** [retail-logistics-core.onrender.com](https://retail-logistics-core.onrender.com)

---

## Overview

RedCart is a complete online store — not a demo. It handles real product inventory, real checkout and payments, real customer accounts, and a real AI assistant that customers actually talk to while shopping. Built from the ground up while learning Django, with each feature shipped, tested, and debugged against live traffic.

---

## 🤖 AI Shopping Assistant

The centerpiece feature: a chatbot built on Groq, designed to be genuinely trustworthy rather than just conversational.

- **Intent-aware routing** — greetings, small talk, product questions, policy questions, and order lookups are each handled differently, so the bot doesn't dump the whole catalog into a reply to "hi"
- **Retrieval-augmented knowledge base** — shipping, returns, warranty, and payment questions are answered from real policy documents, not invented on the fly
- **Guardrails** — the bot will never pretend to add something to your cart, invent a discount, or claim an item is out of stock when it isn't; it's built to say "I don't know" rather than guess
- **Persistent conversation history** — a full sidebar lets both logged-in users and guests revisit past chats, backed by real database storage, not just browser session state
- **Rate limiting and response validation** — protects against abuse and automatically retries responses that come back malformed
- **Direct database order lookups** — order status and tracking numbers are pulled straight from the database, never guessed by the AI

An `evaluate.py` regression suite checks all of the above automatically after any change.

---

## 🛡️ Review Fraud Detection

A tiered fraud-scoring system runs on every review and comment:

- Flags near-duplicate text copied across reviews, review bursts on a single product, brand-new accounts posting immediately, and generic text paired with extreme ratings
- High-confidence fraud is auto-hidden pending staff approval; borderline cases stay published but are flagged for manual review — genuine customer feedback is never silently buried on a false positive
- Full moderation queue built into the Django admin, with one-click approve/hide actions

---

## 🔑 Core Platform Features

- **Authentication** — email/password plus Google OAuth (via django-allauth)
- **Payments** — Paystack integration for card, bank transfer, and wallet payments; escrow-style buyer protection on orders
- **Order management** — full order lifecycle (pending → confirmed → shipped → delivered), tracking numbers, PDF invoices
- **Product catalog** — categories, flash sales with live countdown timers, price history tracking, stock/variant management
- **Wishlist, reviews & ratings, product recommendations** (AI-assisted, using the same Groq integration as the chatbot)
- **Support system** — ticketed customer support, FAQ system, contact form
- **Notifications** — in-app notification center with read/unread tracking
- **Wallet system** — internal wallet balance with top-up and spend tracking
- **Newsletter** — subscribe/unsubscribe with confirmation emails

---

## 📂 Project Structure

```
products/
    models.py             # Product, Order, Review, ChatConversation, and all core models
    views.py               # Request handling for the whole storefront
    utils.py                # Chatbot logic, email sending, stock management
    prompts.py             # Centralized AI system prompts
    rag.py                    # Lightweight document retrieval for the chatbot
    fraud_detection.py     # Review/comment fraud scoring engine
    knowledge/             # Markdown knowledge base the chatbot searches
    admin.py                # Django admin customization, including moderation tools
templates/                # HTML templates (Bootstrap + Tailwind hybrid)
mywork/                    # Project settings and URL configuration
evaluate.py                # Automated chatbot regression test suite
manage.py
```

---

## 🛠️ Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/peterafolabi-dev/Retail-Logistics-Core.git
   cd Retail-Logistics-Core
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (see `.env.example` if present, or check `settings.py` for required keys — Groq API key, Paystack keys, Google OAuth credentials, database URL).
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

### Running the chatbot test suite
```bash
python evaluate.py
```
Checks intent classification, guardrails, rate limiting, and RAG retrieval. Live model checks (requiring a configured `GROQ_API_KEY`) run automatically if the key is present, and skip gracefully otherwise.

---

## 🚀 Deployment

Deployed on Render, using:
- PostgreSQL for production data (SQLite for local development)
- Gunicorn as the WSGI server
- WhiteNoise for static file serving
- Tailwind CSS compiled at build time via `build.sh`

---

## 👤 Author

Afolabi Peter(Kasperky)
Computer engineering student, FUT Minna — building RedCart solo while learning Django along the way.