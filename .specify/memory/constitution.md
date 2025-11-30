# Constitution for “Physical AI & Humanoid Robotics — Unified Book + RAG Chatbot”  
**Project Name:** Physical-AI & Humanoid Robotics Book + RAG Chatbot  
**Ratification Date:** 2025-11-30  
**Constitution Version:** 1.0.0  

---

## Preamble  

This document defines the foundational, non-negotiable principles and quality standards that govern **every** part of this project—book content, backend code, AI agents, infrastructure, and deployment. All specification, planning and implementation work must comply with these rules.  

Violations must be explicitly justified via constitutional gates; otherwise the work shall be rejected or revised.  

---

## Article I — Library-First & Modular Design  
**MUST** design every functional component (e.g., content rendering, RAG backend, chatbot API, user authentication, personalization logic, translation support) as a separate, reusable library/module.  
**MUST NOT** embed feature-specific logic directly into monolithic application code.  

*Rationale:* This ensures modularity, reuse (e.g. subagents / skills), clear boundaries, and easier maintenance and testing.  

---

## Article II — Spec-Driven & Test-First Workflow  
**MUST** write specifications for every new feature (content chapter, backend endpoint, UI interaction, agent skill, etc.) before planning or writing code.  
**MUST** write tests before implementation (unit tests for libraries, integration tests for RAG + DB + API + UI).  

*Rationale:* Guarantees clarity of intent, predictable behavior, and robust quality control via automated tests.  

---

## Article III — Documentation, Content & Code Quality Standards  
- **MUST** include docstrings / documentation for all public modules, classes, functions, and important architectural decisions (e.g. in ADRs — Architecture Decision Records).  
- **MUST** keep code readable: consistent naming, clear layout, adherence to agreed style, no “magic numbers” or obscure constructs.  
- **MUST** document content chapter metadata (e.g. title, dependencies, language variants) in a structured, machine-readable format (e.g. front-matter for markdown).  

*Rationale:* Ensures maintainability, readability, and transparency for both human collaborators and AI agents.  

---

## Article IV — Content & Deployment Standard (Book + UI)  
**MUST** produce the book using the specified stack: static-site via Docusaurus, deployed to GitHub Pages.  
**MUST** keep the site static for core content (chapters), with dynamic behavior isolated to the embedded RAG-chatbot.  
**MUST NOT** introduce heavy runtime dependencies (e.g. full-blown backend frameworks for static chapters).  

*Rationale:* Keeps content lightweight, performant, easy to deploy and host, while isolating dynamic behavior to well-defined modules.  

---

## Article V — RAG & AI Integrations: Privacy, Security & Data Handling  
- **MUST NOT** store or expose any sensitive user data in plaintext (e.g. hardware/software background, authentication credentials, personal info).  
- **MUST** use environment variables or secure vaults — never hardcode secrets.  
- **MUST** validate and sanitize all user inputs (e.g. on signup, sign-in, content personalization) before processing.  
- **MUST** document and log usage of external resources (e.g. calls to vector-store, database queries), ensuring auditability.  

*Rationale:* Protects user privacy, reduces security risk, and ensures compliance with good security practices.  

---

## Article VI — Reusable Intelligence: Subagents & Agent Skills  
**SHOULD** design recurring behaviors (e.g. translation to Urdu, personalization adjustments, content-based QA, session management) as modular “skills” / subagents using Spec‑Kit Plus + Claude Code.  
**MAY** reuse those across chapters, features and future projects.  

*Rationale:* Encourages DRY, reuse, simpler upgrades and consistent behavior across the project; aligns with AI-native design philosophy.  

---

## Article VII — Internationalization & Personalization Support  
- **MUST** support multilingual content (English + Urdu) where required.  
- **MUST** allow content personalization at user level (based on background collected at signup).  
- **MUST** separate content variants (e.g. English, Urdu, personalized) in clearly organized structure (e.g. distinct directories, metadata flags).  

*Rationale:* Ensures scalable support for different user preferences and learning backgrounds without ad-hoc duplication or confusion.  

---

## Article VIII — Simplicity & Minimalism  
**SHOULD** limit the number of top-level projects/components (e.g. at most 3–4: book, backend API, vector-store service, auth module).  
**MUST NOT** over-engineer or over-abstract (e.g. avoid unnecessary wrapper layers over frameworks).  
**MUST** avoid future-proofing speculation — build for known requirements first; defer unknown features until explicitly specified.  

*Rationale:* Prevents complexity creep, reduces maintenance overhead, and keeps architecture clear and manageable.  

---

## Article IX — Version Control, Release & Traceability  
- **MUST** version-control all source, content, specs, tests, data-schemas and configuration in a Git repository.  
- **MUST** tag releases (e.g. v1.0.0) when publishing updates to the book or backend.  
- **MUST** record all architectural decisions and amendments to the constitution or major modules (e.g. via ADRs or commit messages).  

*Rationale:* Ensures reproducibility, accountability and traceability over time — critical for long-term maintenance and collaboration.  

---

## Amendment Process  
To modify this constitution: create a proposal outlining the change, justify why existing Articles are insufficient, and bump the semantic version (e.g. 1.0.0 → 1.1.0). All changes must be reviewed and approved.
