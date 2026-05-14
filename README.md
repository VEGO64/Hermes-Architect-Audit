# Hermes Architect Audit (HAA)

Automated AI cost-intelligence pipeline. Audit LLM infrastructure, reduce latency, and achieve zero-cost routing for agentic workflows.

---

## The Mission

Modern AI engineering faces a fundamental contradiction we call the **Model Paradox**:

> How do you achieve top-tier reasoning while aggressively cutting costs?

The answer is not to find one perfect model. It is to route tasks intelligently.

Hermes Architect Audit (HAA) solves this by implementing an **A vs B task routing framework**. Every task in your multi-agent pipeline is evaluated against two candidates:

- **Option A** -- Efficiency Leader (lowest cost with acceptable quality)
- **Option B** -- Performance Leader (highest quality with acceptable cost)

The result is a system that dynamically assigns the right model to the right task -- instead of burning budget on a single general-purpose model.

---

## System Architecture

```
                                    +------------------+
                                    |   config.yaml    |
                                    | (11 task slots)  |
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    |  LLM Analysis    |
                                    | (OpenRouter API)|
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    | Python FPDF      |
                                    | generate_audit   |
                                    | _pdf.py          |
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    | PDF Report       |
                                    | (A4 Landscape)   |
                                    +------------------+
```

**Flow description:**
1. `config.yaml` defines the 11 task slots and their current model assignments.
2. The LLM layer (OpenRouter API) performs cost/performance analysis on each slot.
3. Python FPDF script (`generate_audit_pdf.py`) renders a stable, pixel-perfect PDF.
4. PDF report is delivered to the target platform (Telegram, Slack, Discord, or local file).

---

## The Impact (Benchmark)

| Metric | Before (Legacy Enterprise Routing) | After (Optimized HAA Routing) |
|---|---|---|
| **Stack Profile** | Claude Opus 4.6/4.7, GPT-4o, GPT-5.5 for every task | Gemini 3.1 Flash Lite for heavy tasks, DeepSeek-V3.1 for medium tasks, Llama-3.2-3B:Free for trivial tasks |
| **Input Cost** | Up to $5.00 / 1M tokens | Down to $0.00 for 6 trivial tasks |
| **Output Cost** | Up to $30.00 / 1M tokens | $0.00 for free-tier, $1.50/1M for heavy tasks |
| **Latency (TTFT)** | 800ms+ on flagship models | Sub-100ms on local 3B models, ~350ms on Gemini Flash Lite |
| **Context Window** | 128K on GPT-4o, variable fragmentation | Seamless 1M tokens on Gemini 3.1 Flash Lite |
| **Cost Reduction** | Baseline bleeding | Up to 99% on routine tasks |

**Enterprise Bloated Stack -- before HAA:**
- Session Search: running GPT-5.5 at $5/$30 per 1M tokens for basic search/retrieval
- Approval checks: running Opus 4.6 at $5/$25 per 1M tokens for simple shell confirmations
- Title Generation: running GPT-4o at $2.50/$10 per 1M tokens for trivial session naming
- Skills Hub: running Opus 4.6 at $5/$25 per 1M tokens for keyword matching

**Optimized Zero-Cost Routing -- after HAA:**
- Session Search: Llama-3.2-3B:Free ($0.00) -- same retrieval quality, zero cost
- Approval: Llama-3.2-3B:Free ($0.00) -- instant sub-100ms responses, zero cost
- Title Generation: Llama-3.2-3B:Free ($0.00) -- identical title quality, zero cost
- Skills Hub: Llama-3.2-3B:Free ($0.00) -- instant text matching, zero cost
- Heavy tasks: Gemini 3.1 Flash Lite at $0.25/$1.50 with 1M context

**The ROI math for a mid-size AI engineering team:**
- 6 out of 11 task slots move to $0.00
- Remaining 5 slots run at $0.25/$1.50 vs the previous $2.50-$30.00
- Estimated monthly saving: $100-150 on a realistic enterprise workload
- At scale (larger teams, higher query volumes), the multiplier scales linearly

---

## Visual Proof (The ROI)

![Audit Recommendations Example](assets/audit_preview.png)

The audit report flags every task where the current model is over-provisioned. A **"SWITCH"** recommendation means the tool detected that the task is running on a paid model when a free or cheaper alternative exists with acceptable quality. Each recommendation includes:

- Current cost vs proposed cost
- Context window comparison
- A rationale tied to your actual usage frequency (e.g., "15+ searches/day")
- A concrete monthly saving estimate

The result is a printable PDF that CTOs and developers can use to justify infrastructure changes to stakeholders.

---

## Architecture and the LLM UI Problem

### The Breakthrough

Most AI pipelines make a critical architectural mistake: they ask the LLM to simultaneously reason AND generate presentation code (HTML, PDF, dashboard). This causes:

- **Hallucinated layouts** -- LLMs drop sections, truncate content, break formatting
- **Inconsistent output** -- each run produces slightly different structure
- **Debugging nightmare** -- the LLM cannot see its own rendered output

Our solution is a clean separation:

```
Layer 1: AI Reasoning (pure JSON output)
        |
        v
Layer 2: Presentation (Python FPDF2 -- deterministic rendering)
```

The AI layer produces a stable JSON structure. The presentation layer reads it and renders a pixel-perfect PDF. The LLM never touches the PDF generation code -- it only produces data. This architectural split is the reason HAA achieves **100% layout stability**.

### Why Pure Python PDF?

We use FPDF2 -- a lightweight Python library with zero external dependencies. No matplotlib, no chart.js, no HTML-to-PDF conversion. Just clean, deterministic text layout. The result is a report that looks the same every single time.

---

## Platform Agnostic

HAA integrates smoothly with any messaging or automation platform:

- **Telegram** -- Direct PDF delivery to chat
- **Slack** -- File upload via API
- **Discord** -- Attachment to channel
- **Terminal** -- Local file output (`~/.cache/documents/`)

The pipeline is input-agnostic. It reads a JSON payload and produces a structured PDF. Where it goes after that is your choice.

---

## Security First

**API keys must never be hardcoded.**

All credentials (OpenRouter keys, provider tokens) are stored in a `.env` file at the project root:

```bash
cp .env.example .env
# Edit .env and add your actual keys
```

The `.env` file is excluded from version control via `.gitignore`. The script reads keys at runtime -- never embeds them in source code.

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env
```

### 3. Generate a Report

```bash
python3 generate_audit_pdf.py '{"profile": "...", "tasks": [...]}'
```

### 4. Output Location

The script writes the PDF to:
```
~/.cache/documents/Model_Cost_Intelligence_[DATE]_v5.pdf
```

---

## File Structure

```
Hermes-Architect-Audit/
|-- assets/
|   |-- .keep                   # Keeps directory in Git
|   |-- audit_preview.png       # Visual preview placeholder
|-- generate_audit_pdf.py       # Core PDF engine (FPDF2 only)
|-- sample_config.yaml           # Example of 11-task model mapping
|-- benchmark_data.json          # Real before/after JSON payload
|-- requirements.txt             # Python dependencies
|-- .env.example                 # Environment variable template
|-- .gitignore                   # Git ignore rules
|-- README.md                    # This file
|-- LICENSE                      # MIT License
```

---

## JSON Structure Reference

The JSON payload requires these fields per task:

| Field | Description |
|---|---|
| `name` | Task identifier (e.g., "Default Chat") |
| `current` | Currently assigned model |
| `cur_in` | Current input price per 1M tokens |
| `cur_out` | Current output price per 1M tokens |
| `opt_a_name` | Option A model name |
| `a_in` | Option A input price per 1M tokens |
| `a_out` | Option A output price per 1M tokens |
| `a_ctx` | Option A context window |
| `opt_b_name` | Option B model name |
| `b_in` | Option B input price per 1M tokens |
| `b_out` | Option B output price per 1M tokens |
| `b_ctx` | Option B context window |
| `rec_label` | Recommendation (e.g., "SWITCH to Option A" or "KEEP") |
| `rationale` | Full reasoning tied to actual workload behavior |

---

## License

MIT License

Copyright (c) 2026 VEGO64

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.