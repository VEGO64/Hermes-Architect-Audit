# Hermes Architect Audit (HAA)

Automated cost-intelligence pipeline for **any multi-agent LLM stack**.  
Audit your model assignments, eliminate budget waste, and route tasks intelligently.

> **Primary Reference Implementation:** [Hermes Agent](https://hermes-agent.nousresearch.com)  
> Compatible with: LangChain, CrewAI, AutoGen, or custom agent pipelines

---

## The Mission

Modern AI engineering faces a fundamental contradiction I call the **Model Paradox**:

> How do you achieve top-tier reasoning while aggressively cutting costs?

The answer is not to find one perfect model. It is to route tasks intelligently.

HAA solves this with an **A vs B task routing framework**. Every task in your agent pipeline is evaluated against two candidates:

- **Option A** — Efficiency Leader (lowest cost with acceptable quality)
- **Option B** — Performance Leader (highest quality with acceptable cost)

The result is a system that dynamically assigns the right model to the right task — instead of burning budget on one general-purpose model.

---

## Personalized for Your Actual Usage

Most cost audits give generic advice. HAA is different — it evaluates based on **your specific behavior profile**:

```json
{
  "profile": "AI Engineering Lead. 60% coding, 25% research, 15% documentation.
               15+ daily searches, compress every session, use skills 10x/day.",
  "profile_detail": "GPT-5.5 at $5/$30 on Session Search, Opus 4.6 at $5/$25 on Approval..."
}
```

| Your Metric | Impact on Cost Calculation |
|---|---|
| Task frequency (daily searches, skill calls) | Multiplied by price per call → real monthly waste |
| Session size / compression needs | Determines whether you need 1M+ context or 128K is fine |
| Reasoning depth required | Flagship for Curator vs free 3B for Title Generation |

The audit doesn't say "Opus is expensive." It says: *"You do 15+ searches/day on GPT-5.5 at $5/$30 — that's $60-80/month on pure keyword matching."*

---

## Continuous Monitoring (Cron Job)

One audit is a snapshot. **Budgets leak over time** as usage patterns shift and new models appear.

HAA supports scheduled re-evaluation via Cron Jobs:

```
Schedule: Every 14 days
Action:  Fetch current prices from OpenRouter API
         Analyze your recent usage profile
         Generate updated PDF with new recommendations
Delivery: Telegram, Slack, Discord, or local file
```

This turns a one-time report into a **living cost monitor** — without you lifting a finger.

---

## Market Adaptation

Model pricing changes weekly:

| Month | Event | Impact |
|---|---|---|
| Today | Gemini Flash Lite at $0.25/$1.50 | — |
| Next month | New free model (e.g., Ring 3.0) | Previous recommendation becomes outdated |
| Next quarter | Opus price drop, GPT-6 launch | New A/B candidates emerge |

A cron-enabled HAA catches these shifts automatically. The report updates itself to recommend the **current cheapest adequate model** — not the one that was cheapest when you first ran it.

---

## System Architecture

```
                                    +------------------+
                                    |   JSON Payload   |
                                    | (your tasks +    |
                                    |  behavior profile)|
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    |  LLM Analysis    |
                                    | (OpenRouter API) |
                                    +--------+---------+
                                             |
                                             v
                                    +------------------+
                                    | Python FPDF2     |
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
1. A JSON payload defines your tasks, current models, pricing, and behavior profile.
2. The LLM layer analyzes every slot for cost-vs-capability fit.
3. Python FPDF2 renders a stable, pixel-perfect PDF with vertical card layout.
4. PDF is delivered to your platform of choice (Telegram, Slack, Discord, or local file).

---

## The Impact (Benchmark)

### The Problem: Legacy Enterprise Routing

Most enterprise AI stacks default to **one model for everything** — Claude Opus 4.6/4.7, GPT-4o, and GPT-5.5 on every task, even trivial ones. The result is a budget hemorrhage:

- Session Search: GPT-5.5 at $5.00 Input / $30.00 Output per 1M tokens for basic retrieval
- Approval checks: Opus 4.6 at $5.00 / $25.00 per 1M tokens for simple shell confirmations
- Title Generation: GPT-4o at $2.50 / $10.00 per 1M tokens for trivial naming tasks
- Skills Hub: Opus 4.6 at $5.00 / $25.00 per 1M tokens for keyword matching

This is not a tooling problem. This is a routing problem.

### The Solution: Optimized HAA Routing

HAA detects this waste automatically and recommends the correct model per task:

- **Session Search** → Llama-3.2-3B:Free ($0.00 / $0.00) — zero cost, sub-100ms latency
- **Approval** → Llama-3.2-3B:Free ($0.00 / $0.00) — zero cost, sub-100ms
- **Title Generation** → Llama-3.2-3B:Free ($0.00 / $0.00) — zero cost, identical quality
- **Skills Hub** → Llama-3.2-3B:Free ($0.00 / $0.00) — zero cost, instant matching
- **Heavy tasks** (long-context coding, complex reasoning) → Gemini 3.1 Flash Lite at $0.25 / $1.50 with 1M context
- **Medium tasks** (tool traces, memory pruning) → DeepSeek-V3.1 at $0.15 / $0.75

### The ROI

| Metric | Legacy Routing | HAA Optimized |
|---|---|---|
| **Stack** | Opus 4.6/4.7, GPT-4o, GPT-5.5 on every task | Free 3B for trivial, Flash Lite for heavy, DeepSeek for medium |
| **Input Cost** | Up to $5.00 / 1M tokens | Down to $0.00 on 6 task slots |
| **Output Cost** | Up to $30.00 / 1M tokens | $0.00 for free-tier, $1.50 / 1M for heavy tasks |
| **Latency (TTFT)** | 800ms+ on flagship models | Sub-100ms on local 3B models |
| **Context Window** | 128K fragmentation on GPT-4o | Seamless 1M+ tokens on Gemini Flash Lite |
| **Cost Reduction** | Baseline bleeding | Up to 99% on routine tasks |

**Real monthly impact for a single user:**
- 6 out of 11 task slots go to **$0.00** (free models)
- Remaining 5 route to **$0.15-$0.25 / 1M input**
- Estimated saving: **$100-150/month**
- At scale (10 agents): **$1,000-1,500/month saved**

---

## Smart Compromise: Overkill vs. Hallucination Risk

Not every task should go to the cheapest model:

### Trivial - Zero Cost (Pure Overkill)

**Compression: Opus 4.6 ($5/$25) → Ring 2.6-1t:Free ($0/$0)**

Session compression is structural summarization — no creativity needed. Ring 2.6 is a thinking model built for exactly this. Zero quality regression, zero cost.

**Approval: GPT-5.5 ($5/$30) → Llama 3B ($0/$0)**

Shell safety checks don't need frontier reasoning. Llama 3B responds in sub-100ms vs 800ms+, with identical safety logic.

### Heavy - Guarded Model (Anti-Hallucination)

**Curator: Opus 4.7 ($5/$25) → DeepSeek V3.2 ($0.252/$0.378)**

Memory pruning decisions hallucinate if the model lacks instruction alignment — a 3B model dropping a memory entry corrupts session state. DeepSeek V3.2 (33x cheaper than Opus 4.7) provides the rigor needed without going free.

**MCP Tooling: GPT-4o ($2.50/$10) → Gemini Flash Lite ($0.25/$1.50)**

Flash Lite keeps 1M context — critical for long tool traces. GPT-4o's 128K would truncate multi-step execution logs. The recommendation preserves context integrity over raw cost savings.

---

## The CTO Blindspot

**The biggest silent drain: running flagship models on tasks with zero reasoning requirement.**

| Task | Reasoning Needed? | What It Actually Does |
|---|---|---|
| Session Search | ❌ | Keyword retrieval |
| Title Generation | ❌ | Auto-naming sessions |
| Skills Hub | ❌ | Text matching |
| Approval | ❌ | Safety pattern check |
| Compression | ❌ | Log summarization |
| Triage Specifier | ❌ | Directory routing |

These 6 tasks consume **~55% of budget** while contributing **~0% of reasoning value**.

> **The formula:** If a human could do the task in <2 seconds with no training, do not pay frontier-model prices for it.

---

## Visual Proof

![Enterprise Audit — Before](assets/before_audit.png)
[View the Full Generated Audit PDF](assets/Audit_Report.pdf)

---

## Architecture and the LLM UI Problem

Most AI pipelines make a critical architectural mistake: asking the LLM to simultaneously reason AND generate presentation code (HTML, PDF, dashboard). This causes:

- **Hallucinated layouts** — LLMs drop sections, truncate content, break formatting
- **Inconsistent output** — each run produces different structure
- **Debugging nightmare** — the LLM cannot see its own rendered output

My solution is a clean separation:

```
Layer 1: AI Reasoning (pure JSON output)
        |
        v
Layer 2: Presentation (Python FPDF2 — deterministic rendering)
```

The AI layer produces a stable JSON structure. The presentation layer reads it and renders a pixel-perfect PDF. The LLM never touches PDF generation — it only produces data.

### Why Pure Python PDF?

I use FPDF2 — a lightweight library with zero external dependencies. No matplotlib, no chart.js, no HTML-to-PDF conversion. Just deterministic text layout. The result is a report that looks the same every single time.

---

## Platform Agnostic

HAA integrates with any messaging or automation platform:

- **Telegram** — Direct PDF delivery to chat
- **Slack** — File upload via API
- **Discord** — Attachment to channel
- **Terminal** — Local file output

The pipeline is input-agnostic. It reads JSON and produces a structured PDF. Where it goes after that is your choice.

---

## Integration with Hermes Agent

HAA was built as the reference implementation for [Hermes Agent](https://hermes-agent.nousresearch.com) — an open-source AI agent that runs on Telegram.

For Hermes Agent users, setup takes seconds:

1. Run the audit with the provided sample data
2. Apply the recommended model changes to your `config.yaml`
3. Set up a Cron Job to regenerate the report every 14 days

The `sample_input.json` maps directly to Hermes Agent's auxiliary task slots:

| Slot | Current (Before) | Recommended (After) |
|---|---|---|
| Default Chat | Opus 4.6 ($5/$25) | Flash Lite ($0.25/$1.50) |
| Vision | GPT-4o ($2.50/$10) | Flash Lite ($0.25/$1.50) |
| Web Extract | GPT-4o ($2.50/$10) | Flash Lite ($0.25/$1.50) |
| Compression | Opus 4.6 ($5/$25) | Ring 2.6:Free ($0/$0) |
| Session Search | GPT-5.5 ($5/$30) | Ring 2.6:Free ($0/$0) |
| Skills Hub | Opus 4.6 ($5/$25) | Ring 2.6:Free ($0/$0) |
| Approval | GPT-5.5 ($5/$30) | Ring 2.6:Free ($0/$0) |
| MCP Tooling | GPT-4o ($2.50/$10) | Ring 2.6:Free ($0/$0) |
| Title Gen | GPT-4o ($2.50/$10) | Ring 2.6:Free ($0/$0) |
| Triage | Gemini 3.1 Pro ($2/$12) | Ring 2.6:Free ($0/$0) |
| Curator | Opus 4.7 ($5/$25) | DeepSeek V3.2 ($0.252/$0.378) |

---

## Security

**API keys must never be hardcoded.** All credentials are stored in a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your actual keys
```

The `.env` is excluded from version control via `.gitignore`. The script reads keys at runtime — never embeds them in source.

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

### 3. Run with Sample Data (Zero Configuration)

```bash
python3 generate_audit_pdf.py "$(cat sample_input.json)"
```

The script automatically creates `./output/` and writes the PDF there.

### 4. Run with Custom JSON

```bash
python3 generate_audit_pdf.py '{"profile": "...", "tasks": [...]}'
```

See [JSON Structure Reference](#json-structure-reference) below.

### 5. Output Location

```bash
./output/Model_Cost_Intelligence_[DATE]_v5.pdf
```

---

## Custom Integration (Non-Hermes)

HAA accepts any JSON payload following the schema below. You define:
- Your own task names and models
- Current pricing per 1M tokens (from any provider)
- Two alternative recommendations (A and B)
- Your behavior profile for personalized cost calculations

```json
{
  "profile": "Your usage description. Mention task frequency for accurate compounding.",
  "profile_detail": "Optional before/after summary.",
  "tasks": [
    {
      "name": "Your Task Name",
      "current": "provider/model-name",
      "cur_in": "input_price_per_1M",
      "cur_out": "output_price_per_1M",
      "opt_a_name": "provider/option-a-model",
      "a_in": "0.00",
      "a_out": "0.00",
      "a_ctx": "128K",
      "opt_b_name": "provider/option-b-model",
      "b_in": "0.25",
      "b_out": "1.50",
      "b_ctx": "1M",
      "rec_label": "SWITCH to Option A",
      "rationale": "Why this switch makes sense for YOUR workload."
    }
  ]
}
```

---

## File Structure

```
Hermes-Architect-Audit/
|-- assets/
|   |-- .keep                   # Keeps directory in Git
|   |-- before_audit.png        # Audit detection screenshot
|   |-- Audit_Report.pdf        # Full generated PDF report
|-- output/                      # Auto-created on first run
|   |-- Model_Cost_Intelligence_[DATE]_v5.pdf
|-- generate_audit_pdf.py       # Core PDF engine (FPDF2 only)
|-- sample_config.yaml           # Example of 11-task model mapping
|-- sample_input.json            # Enterprise bloated stack test payload
|-- benchmark_data.json          # Real before/after JSON payload
|-- requirements.txt             # Python dependencies
|-- .env.example                 # Environment variable template
|-- .gitignore                   # Git ignore rules
|-- README.md                    # This file
|-- LICENSE                      # MIT License
```

---

## JSON Structure Reference

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
| `rec_label` | Recommendation ("SWITCH to Option A" or "KEEP") |
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
furnished to do so, subject to the following conditions.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.