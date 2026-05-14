# Hermes Architect Audit (HAA)

Automated AI cost-intelligence pipeline. Audit LLM infrastructure, reduce latency, and achieve zero-cost routing for agentic workflows.

---

## The Mission

Modern AI engineering faces a fundamental contradiction we call the **Model Paradox**:

> How do you achieve top-tier reasoning while aggressively cutting costs?

The answer is not to find one perfect model. It is to route tasks intelligently.

Hermes Architect Audit (HAA) solves this by implementing an **A vs B task routing framework**. Every task in your multi-agent pipeline is evaluated against two candidates:

- **Option A** — Efficiency Leader (lowest cost with acceptable quality)
- **Option B** — Performance Leader (highest quality with acceptable cost)

The result is a system that dynamically assigns the right model to the right task — instead of burning budget on a single general-purpose model.

---

## The Impact (Benchmark)

| Metric | Before (Legacy Auto-Routing) | After (Optimized HAA Routing) |
|---|---|---|
| **Default Model** | Gemini 2.0 Flash for everything | Gemini 3.1 Flash Lite (heavy) + Llama 3.2 3B Free (trivial) |
| **Input Cost** | $0.10 / 1M tokens | Down to $0.00 for 4 trivial tasks |
| **Output Cost** | $0.40 / 1M tokens | $0.00 for free-tier tasks |
| **Latency (TTFT)** | ~800ms | Under 350ms on optimized tasks |
| **Context Window** | 128K chunking | Seamless 1.05M tokens |
| **Monthly Savings** | Baseline | ~30-40% cost reduction |

**Real-world example:**
- Session Search task: was paying Gemini 2.0 Flash ($0.10/$0.40) → switched to Llama 3.2 3B Free ($0.00/$0.00)
- This single task runs 15+ times per day. At that frequency, the annual saving is significant.

---

## Architecture and the LLM UI Problem

### The Breakthrough

Most AI pipelines make a critical architectural mistake: they ask the LLM to simultaneously reason AND generate presentation code (HTML, PDF, dashboard). This causes:

- **Hallucinated layouts** — LLMs drop sections, truncate content, break formatting
- **Inconsistent output** — each run produces slightly different structure
- **Debugging nightmare** — the LLM cannot see its own rendered output

Our solution is a clean separation:

```
Layer 1: AI Reasoning (pure JSON output)
        ↓
Layer 2: Presentation (Python FPDF2 — deterministic rendering)
```

The AI layer produces a stable JSON structure. The presentation layer reads it and renders a pixel-perfect PDF. The LLM never touches the PDF generation code — it only produces data. This architectural split is the reason HAA achieves **100% layout stability**.

### Why Pure Python PDF?

We use FPDF2 — a lightweight Python library with zero external dependencies. No matplotlib, no chart.js, no HTML-to-PDF conversion. Just clean, deterministic text layout. The result is a report that looks the same every single time.

---

## Platform Agnostic

HAA integrates smoothly with any messaging or automation platform:

- **Telegram** — Direct PDF delivery to chat
- **Slack** — File upload via API
- **Discord** — Attachment to channel
- **Terminal** — Local file output (`~/./cache/documents/`)

The pipeline is input-agnostic. It reads a JSON payload and produces a structured PDF. Where it goes after that is your choice.

---

## Security First

**API keys must never be hardcoded.**

All credentials (OpenRouter keys, provider tokens) are stored in a `.env` file at the project root:

```
OPENROUTER_API_KEY=sk-or-your-key-here
```

The `.env` file is excluded from version control via `.gitignore`. The script reads keys at runtime — never embeds them in source code.

---

## How to Run

### Prerequisites

```bash
pip install fpdf2
```

### Execution

```bash
python3 generate_audit_pdf.py '{"profile": "...", "tasks": [...]}'
```

### Output

The script writes the PDF to:
```
~/.cache/documents/Model_Cost_Intelligence_[DATE]_v5.pdf
```

### JSON Structure

The JSON payload requires these fields per task:

```
name          — Task identifier (e.g., "Default Chat")
current       — Currently assigned model
cur_in        — Current input price per 1M tokens
cur_out       — Current output price per 1M tokens
opt_a_name    — Option A model name
a_in          — Option A input price per 1M tokens
a_out         — Option A output price per 1M tokens
a_ctx         — Option A context window
opt_b_name    — Option B model name
b_in          — Option B input price per 1M tokens
b_out         — Option B output price per 1M tokens
b_ctx         — Option B context window
rec_label     — Recommendation (e.g., "SWITCH to Option A" or "KEEP")
rationale     — Full reasoning tied to actual workload behavior
```

---

## File Structure

```
Hermes-Architect-Audit/
├── generate_audit_pdf.py   # Core PDF engine (FPDF2 only)
├── sample_config.yaml       # Example of 11-task model mapping
├── benchmark_data.json      # Real before/after JSON payload
├── README.md                # This file
└── LICENSE                  # MIT License
```

---

## License

MIT License

Copyright (c) 2026 VEGO64

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.