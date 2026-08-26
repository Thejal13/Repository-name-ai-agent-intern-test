# Aster & Row — Reliable RAG Support Agent

A small, reliability-focused customer support agent for Aster & Row, a fictional ecommerce company selling bags, drinkware, and travel accessories.

The system combines retrieval over the supplied knowledge base, safe order lookup, document precedence, multi-turn conversation handling, privacy protection, prompt-injection resistance, and safe human handoff.

The goal is not to build the largest possible agent. The goal is to build a small system that behaves safely and predictably on messy real-world support data.

---

## 1. Problem

The support agent is designed to handle common ecommerce support questions while avoiding unsupported claims and unsafe disclosure of internal information.

The supplied knowledge base contains:

- Current and superseded policies
- Internal notes
- Conflicting active sources
- Product information
- Shipping information
- Warranty information

The operational dataset contains mock order information, including both customer-safe and internal fields.

The main design goals are:

1. Reliable and grounded answers
2. Correct document precedence
3. Safe order lookup
4. Privacy protection
5. Safe abstention when information is insufficient
6. Human handoff when required
7. Reliable multi-turn behavior

---

## 2. Architecture

```text
                    ┌──────────────────────┐
                    │      User / CLI      │
                    └──────────┬───────────┘
                               │
                               v
                    ┌──────────────────────┐
                    │     SupportAgent     │
                    │      agent.py        │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────┘       └──────────┐
                 │                             │
                 v                             v
      ┌────────────────────┐       ┌────────────────────┐
      │ Knowledge Retrieval│       │   Order Lookup     │
      │  retrieval.py      │       │    orders.py      │
      └──────────┬─────────┘       └──────────┬─────────┘
                 │                             │
                 v                             v
      ┌────────────────────┐       ┌────────────────────┐
      │ knowledge-base/    │       │ data/orders.json   │
      │ Markdown documents │       │                    │
      └──────────┬─────────┘       └────────────────────┘
                 │
                 v
       Safety / precedence /
       groundedness checks
                 │
                 v
       Customer-safe response
Customer-safe response
```

### Main components

```text
app/
├── agent.py       # Agent behavior and response routing
├── retrieval.py   # Knowledge-base indexing and retrieval
├── orders.py      # Safe order lookup
└── main.py        # CLI interface
```

---

## 3. Technology

- Python 3.13
- Command-line interface
- Markdown knowledge base
- JSON operational order dataset
- Python-based retrieval
- OpenAI API integration
- pytest for regression testing

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
