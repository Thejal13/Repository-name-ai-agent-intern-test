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
