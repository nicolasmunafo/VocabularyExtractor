# Vocabulary Extractor

An automated Python pipeline designed to extract text from `.jpg` image files using EasyOCR, translate extracted terms using a local Ollama LLM model, and sync structured results directly into Google Sheets.

## Architecture & Workflow

```text
[ Directory (.jpg) ] ──> [ EasyOCR ] ──> [ Local Ollama ] ──> [ Google Sheets API ]
