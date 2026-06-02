# Agentic TODO List

> 🚧 Work in progress

A todo-list app showing how any CRUD API can gain a conversational LLM interface without changing the backend.

## Concept

The same FastAPI backend powers two interfaces:

- **Traditional frontend** — classic HTML/JS CRUD UI
- **LLM chat interface** — an AI agent that manages your todos conversationally via tool calling

The goal is to demonstrate that any well-structured API can be extended with a conversational layer without touching the backend.

## Stack

- **Backend:** Python + FastAPI + SQLite
- **Frontend:** Vanilla HTML/CSS/JS
- **LLM integration:** in progress

## Structure

```
backend/    # FastAPI
frontend/   # Static HTML/JS/CSS UI
```

## Status

Project under active development. API and frontend are being built first; LLM interface comes next.
