# Aster & Row — Reliable RAG Support Agent

A small, reliability-focused customer support agent for **Aster & Row**, a fictional ecommerce company selling bags, drinkware, and travel accessories.

The system combines knowledge-base retrieval, safe order lookup, document precedence, privacy protection, prompt-injection resistance, safe abstention, human handoff, and multi-turn conversation handling.

The goal is not to build the largest possible agent. The goal is to build a small system that behaves safely and predictably on messy real-world support data.

---

## 1. Problem

The support agent handles common ecommerce support questions while avoiding unsupported claims and unsafe disclosure of internal information.

The supplied knowledge base contains:

- Current and superseded policies
- Internal notes
- Conflicting active sources
- Product information
- Shipping information
- Warranty information
- Support escalation guidance

The operational dataset contains mock order information, including both customer-safe and internal fields.

### Main Design Goals

1. Reliable and grounded answers
2. Correct document precedence
3. Safe order lookup
4. Privacy protection
5. Safe abstention when information is insufficient
6. Human handoff when required
7. Multi-turn conversation handling
8. Prompt-injection resistance

---

## 2. Architecture

```text
                    ┌──────────────────────┐
                    │      User / CLI      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     SupportAgent     │
                    │      agent.py        │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────┘       └──────────┐
                 │                             │
                 ▼                             ▼
      ┌────────────────────┐       ┌────────────────────┐
      │ Knowledge Retrieval│       │   Order Lookup     │
      │  retrieval.py      │       │    orders.py      │
      └──────────┬─────────┘       └──────────┬─────────┘
                 │                             │
                 ▼                             ▼
      ┌────────────────────┐       ┌────────────────────┐
      │ knowledge-base/    │       │ data/orders.json   │
      │ Markdown documents │       │                    │
      └──────────┬─────────┘       └────────────────────┘
                 │
                 ▼
       Safety / precedence /
       groundedness checks
                 │
                 ▼
       Customer-safe response
```

### Main Components

```text
app/
├── agent.py       # Agent behavior and response routing
├── retrieval.py   # Knowledge-base retrieval
├── orders.py      # Safe order lookup
└── main.py        # CLI interface
```

---

## 3. Technology Stack

* Python 3.13
* Command-line interface
* Markdown knowledge base
* JSON operational order dataset
* TF-IDF retrieval
* Cosine similarity
* scikit-learn
* pytest
* python-dotenv
* OpenAI API dependency

The implementation intentionally keeps the architecture small and practical instead of introducing unnecessary production infrastructure.

---

## 4. Repository Structure

```text
.
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   ├── orders.py
│   └── retrieval.py
│
├── data/
│   ├── orders.json
│   └── orders-data-dictionary.md
│
├── knowledge-base/
│   ├── 01-returns-policy-current.md
│   ├── 02-returns-policy-legacy.md
│   ├── 03-final-sale-and-promotions.md
│   ├── 04-damaged-or-wrong-items.md
│   ├── 05-domestic-shipping.md
│   ├── 06-international-shipping.md
│   ├── 07-warranty.md
│   ├── 08-order-changes-and-cancellations.md
│   ├── 09-trailplus-membership.md
│   ├── 10-gift-cards-and-price-adjustments.md
│   ├── 11-product-care.md
│   ├── 12-breeze-tumbler-product-card.md
│   ├── 13-support-escalation.md
│   └── 14-internal-content-migration-notes.md
│
├── evaluation/
│   ├── visible-cases.json
│   └── run_visible_cases.py
│
└── tests/
    └── test_agent.py
```

---

## 5. Setup

Create and activate a virtual environment:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

No real API keys or secrets should be committed to the repository.

---

## 6. Running the Agent

Run the command-line support agent:

```bash
python3.13 -m app.main
```

The agent accepts customer questions interactively.

Example:

```text
Aster & Row Support Agent
Type 'exit' to quit.

You: How long does a regular customer have to return an unused backpack?

Agent: Regular customers have 30 calendar days from delivery to return an unused backpack.
```

The CLI can also handle order lookup and safety-related cases such as missing order IDs, damaged final-sale items, insufficient information, and human handoff.

---

## 7. Testing and Evaluation

### Unit Tests

Run:

```bash
python3.13 -m pytest -q
```

Current result:

```text
9 passed
```

### Visible Evaluation

Run:

```bash
python3.13 -m evaluation.run_visible_cases
```

Current result:

```text
RESULT: 20/20 cases passed
```

### Evaluation Coverage

The evaluation suite covers:

* Retrieval quality
* Groundedness
* Document precedence
* Tool use
* Tool reliability
* Privacy
* Prompt-injection resistance
* Safe abstention
* Human handoff
* Multi-turn conversation handling
* Source conflicts
* Order ID normalization

---

## 8. Safety and Privacy

The order lookup exposes only customer-safe fields.

The system does not expose:

* Customer email addresses
* Customer addresses
* Internal notes
* Risk scores
* Fraud information
* Other internal-only order fields

Unknown or malformed order IDs do not result in invented order information.

Cancelled and returned orders do not expose stale shipping or delivery information.

When information is unavailable or conflicting, the agent recommends human confirmation instead of making an unsupported claim.

---

## 9. Document Precedence and Grounding

The knowledge base contains both active and superseded documents.

The retrieval layer gives preference to current documents and reduces the ranking of legacy and internal documents.

This prevents outdated or unapproved material from becoming the authority for customer-facing answers.

Internal migration notes are treated as untrusted data. Instructions contained inside retrieved documents cannot override the agent's application behavior.

When authoritative sources genuinely conflict, the agent avoids inventing an answer and recommends human confirmation.

---

## 10. Bug Diary

### Bug 1 — Legacy Policy Precedence

The knowledge base contained both a current returns policy and a superseded legacy policy.

The retrieval system was adjusted to prefer current policy documents and penalize legacy and internal documents.

### Bug 2 — Cancelled Order Stale ETA

Cancelled orders could contain historical shipping-related fields.

The order lookup now removes carrier, tracking, delivery, and shipping timestamp information for cancelled and returned orders.

### Bug 3 — Prompt Injection in Retrieved Content

An internal migration document contained instructions attempting to override the support agent and reveal the hidden prompt.

The document is treated as untrusted data and cannot override the active customer policy or application behavior.

### Bug 4 — Order ID Normalization

Users may provide order IDs in lowercase or with surrounding whitespace.

Order IDs are normalized by trimming whitespace and converting them to uppercase before lookup.

### Bug 5 — Deterministic Evaluation Wording

Some evaluation cases check important concepts such as delivery dates, return windows, and escalation requirements.

Responses were adjusted so important grounded facts remain explicit and consistent with the supplied evaluation cases.

---

## 11. Known Limitations

This is a small take-home implementation rather than a production support platform.

Known limitations include:

* Retrieval uses TF-IDF rather than semantic embeddings.
* The interface is CLI-only.
* There is no persistent conversation database.
* Order lookup uses the supplied mock JSON dataset.
* Human handoff is represented in the response rather than integrated with a ticketing system.
* Observability is limited compared with a production tracing system.
* Several high-priority scenarios use deterministic response routing.

For production, I would add stronger metadata-aware retrieval, persistent conversation state, authentication, structured tracing, real support/ticketing integration, and broader adversarial testing.

---

## 12. AI Coding Tools

AI coding assistance was used during development for:

* Debugging Python syntax and indentation issues
* Reviewing test failures
* Improving response handling
* Refining evaluation coverage
* Drafting documentation

AI suggestions were verified by running the Python compiler, unit tests, and visible evaluation suite.

The final implementation was validated through automated tests rather than relying on generated code without verification.

---

## 13. Demo

A short demonstration of the Aster & Row support agent handling:

* Policy retrieval
* Order lookup
* Missing order information
* Damaged-item escalation
* Insufficient information

[▶️ Watch the Aster & Row Support Agent Demo](demo/ai_agent_demo.mp4)
