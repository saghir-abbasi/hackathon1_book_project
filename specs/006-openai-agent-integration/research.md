# Research for Feature 2.4 — OpenAI Agents / ChatKit Integration

## Unresolved Clarifications from Technical Context

### Q1: Frontend Testing Framework

**What we need to know**: Which frontend testing framework (e.g., Jest, Vitest, React Testing Library) should be adopted for the Docusaurus-based client-side chat interface component?

**Suggested Answers**:
| Option | Answer | Implications |
|--------|--------|--------------|
| A      | **Jest with React Testing Library** | Standard choice for React projects, strong community support, good for unit and integration testing of components. |
| B      | **Vitest with React Testing Library** | Faster alternative to Jest, especially for projects using Vite, but a newer ecosystem. |
| C      | **Cypress (for E2E)** | Focuses on end-to-end testing, good for user flow validation but less granular for unit tests. |
| Custom | Provide your own answer | Consider existing project practices or specific Docusaurus recommendations. |

### Q2: Performance Goals for Streaming and Concurrency

**What we need to know**: What are the specific measurable performance goals for the AI assistant's streaming response time and the number of concurrent users it should support?

**Suggested Answers**:
| Option | Answer | Implications |
|--------|--------|--------------|
| A      | **Streaming Response**: P90 latency < 3 seconds; **Concurrency**: 100 concurrent users | Aggressive performance, potentially higher infrastructure cost. |
| B      | **Streaming Response**: P90 latency < 5 seconds; **Concurrency**: 50 concurrent users | Balanced performance, reasonable infrastructure cost. |
| C      | **Streaming Response**: P90 latency < 8 seconds; **Concurrency**: 20 concurrent users | Moderate performance, lower infrastructure cost, suitable for initial launch. |
| Custom | Provide your own answer | Specify exact P90/P95 latency targets and desired concurrent user load. |

### Q3: Expected User and Query Volume

**What we need to know**: What is the expected daily active user (DAU) count and the anticipated average daily query volume for the AI assistant?

**Suggested Answers**:
| Option | Answer | Implications |
|--------|--------|--------------|
| A      | **DAU**: 1,000-5,000; **Queries**: 5,000-25,000 | Requires scalable infrastructure, robust abuse prevention. |
| B      | **DAU**: 100-500; **Queries**: 500-2,500 | Moderate infrastructure, standard abuse prevention. |
| C      | **DAU**: <100; **Queries**: <500 | Minimal infrastructure, basic abuse prevention. |
| Custom | Provide your own answer | Provide specific DAU and average daily query estimates. |

## Research Findings

**Decision**: Frontend Testing Framework: Jest with React Testing Library
**Rationale**: Standard choice for React projects, strong community support, good for unit and integration testing of components. Fits well with Docusaurus being React-based.
**Alternatives considered**: Vitest (newer, but less mature ecosystem for Docusaurus), Cypress (E2E focused, not ideal for unit/integration).

**Decision**: Performance Goals: Streaming Response: P90 latency < 5 seconds; Concurrency: 50 concurrent users
**Rationale**: This provides a balanced performance target with reasonable infrastructure cost, suitable for the current project phase and expected initial load.
**Alternatives considered**: More aggressive targets (higher cost), more moderate targets (lower user experience).

**Decision**: Expected User and Query Volume: DAU: <100; Queries: <500
**Rationale**: Minimal infrastructure requirements and basic abuse prevention are sufficient for the anticipated low user and query volume.
**Alternatives considered**: Higher volume tiers (over-engineering for current needs).