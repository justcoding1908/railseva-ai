# 🚂 RailSeva AI

> Multi-agent AI platform for railway grievance intelligence and predictive maintenance.

## Overview

RailSeva is an AI-powered system that processes railway passenger complaints through a pipeline of 6 specialized agents — classifying issues, looking up policies via RAG, escalating safety-critical complaints, and identifying fault patterns from maintenance history.

## Features

- 🤖 **6-Agent LangGraph Orchestration** — Intake → Classification → Policy → Escalation → Maintenance → Supervisor
- 📚 **RAG over Indian Railways Policy Docs** — Grounded, hallucination-resistant responses
- ⚠️ **Safety Escalation** — Hybrid rule + LLM system for critical complaint flagging
- 🌐 **Multilingual** — Hindi and English complaint processing
- 📊 **Agent Reasoning Trace** — Visual dashboard showing every agent's decision
- 📈 **Fault Pattern Analytics** — Predictive maintenance insights from historical data

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph |
| LLM | Groq (LLaMA 3.3-70b) |
| RAG | FAISS + LangChain |
| Embeddings | sentence-transformers |
| Backend | FastAPI |
| Frontend | React + Vite |
| Deployment | Render + Vercel |

## Architecture

## Project Status
🚧 In active development

## Author
Vaishnavi — CS Undergrad, Manipal University Jaipur