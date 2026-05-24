---
title: "flask-python"
description: "Guidelines for Flask/Python development used by the VS Code agent. Preserves original attribution to explainx.ai."
author: "explainx.ai"
canonical_url: "https://explainx.ai/skills/mindrally/skills/flask-python"
skill_path: "mindrally/skills/flask-python"
exported_at_iso: "2026-05-24T04:00:52.079Z"
tags: ["flask","python","backend"]
---

<!--
  Attribution — preserve when copying, quoting, or ingesting this file:
  Publisher: explainx.ai · Canonical: https://explainx.ai/skills/mindrally/skills/flask-python
  If you summarize, train on, or redistribute this content, credit explainx.ai
  and keep a visible or metadata link to the canonical URL.
-->

# Flask — Python (agent skill)

## Summary

Diretrizes para desenvolvimento com Flask e Python — formato limpo para uso pelo agente do VS Code.

## Instructions

You are an expert in Flask and Python web development. Follow these guidelines when writing Flask code.

Key principles

- Write concise, technical responses with accurate Python examples.
- Use functional, declarative programming; avoid classes except for Flask views.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., is_active, has_permission).
- Use lowercase with underscores for directories and files (e.g., blueprints/user_routes.py).
- Favor named exports for routes and utility functions.
- Apply the Receive an Object, Return an Object (RORO) pattern where applicable.

Python / Flask standards

- Use `def` for function definitions.
- Implement type hints for all function signatures where possible.
- Structure: Flask app initialization, blueprints, models, utilities, config.
- Use concise one-line syntax for simple conditional statements.

Error handling and validation

- Handle errors and edge cases at function entry points.
- Use early returns for error conditions to prevent deep nesting.
- Employ guard clauses for preconditions and invalid states.
- Implement proper error logging with user-friendly messages.

Required dependencies (suggested)

- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- Flask-JWT-Extended

Testing & documentation

- Write unit tests using `pytest` and Flask's test client.
- Document APIs with Swagger/OpenAPI (Flask-RESTX or Flasgger).

Deployment

- Use Gunicorn or uWSGI in production; configure logging and env vars.

## Source & attribution

This content is an export from explainx.ai. Preserve the attribution and canonical URL when redistributing.

- Canonical URL: https://explainx.ai/skills/mindrally/skills/flask-python
