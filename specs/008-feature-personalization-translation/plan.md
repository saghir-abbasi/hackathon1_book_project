# Implementation Plan: Personalization & Translation UI

**Branch**: `008-feature-personalization-translation` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/008-feature-personalization-translation/spec.md`

## Summary

Implement a UI feature that allows users to personalize chapter content based on their background (Software/Hardware) and translate content to Urdu. The feature adds two buttons at the top of each documentation chapter that trigger AI-powered content transformation via the existing Agent API with streaming responses.

## Technical Context

**Language/Version**: TypeScript 5.6, React 19, CSS3
**Primary Dependencies**: Docusaurus 3.9.2, React, existing AgentBridge client
**Storage**: localStorage (client-side preference persistence)
**Testing**: Manual testing, React component tests
**Target Platform**: Web browsers (GitHub Pages static site)
**Project Type**: Web application (frontend-only feature)
**Performance Goals**: UI response < 100ms, streaming content display
**Constraints**: Must work with static Docusaurus site, no backend changes required
**Scale/Scope**: All documentation chapters (~8 chapters currently)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Article | Requirement | Status | Notes |
|---------|-------------|--------|-------|
| I - Modular Design | Separate reusable module | ✅ PASS | ChapterToolbar component + hooks |
| II - Spec-Driven | Spec before code | ✅ PASS | spec.md exists |
| III - Documentation | Docstrings, readable code | ✅ PASS | Will document components |
| IV - Static Content | No heavy runtime deps | ✅ PASS | Client-side only, uses existing API |
| V - Privacy/Security | No plaintext sensitive data | ✅ PASS | localStorage for non-sensitive preference |
| VI - Reusable Intelligence | Modular skills | ✅ PASS | Uses existing Agent API |
| VII - i18n & Personalization | Support multilingual + personalization | ✅ PASS | Core feature requirement |
| VIII - Simplicity | No over-engineering | ✅ PASS | Simple component + localStorage |
| IX - Version Control | Git tracked | ✅ PASS | Feature branch exists |

**All gates PASS** - No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/008-feature-personalization-translation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── agent-api.md     # API contract for personalization/translation
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
docusaurus-book-site/
├── src/
│   ├── components/
│   │   └── ChapterToolbar/           # NEW: Personalization & Translation UI
│   │       ├── index.tsx             # Main toolbar component
│   │       ├── PersonalizeButton.tsx # Personalize button + modal
│   │       ├── TranslateButton.tsx   # Translate to Urdu button
│   │       ├── ContentOverlay.tsx    # Displays transformed content
│   │       └── styles.module.css     # Robotics-themed styling
│   │
│   ├── hooks/
│   │   └── useUserPreferences.ts     # NEW: localStorage hook for background
│   │
│   ├── theme/
│   │   └── DocItem/
│   │       └── Layout/
│   │           └── index.tsx         # SWIZZLE: Wrap with ChapterToolbar
│   │
│   └── agent-client/
│       └── agentBridge.js            # EXISTING: Reuse for API calls
│
└── static/
    └── img/                          # Any new icons if needed
```

**Structure Decision**: Frontend-only implementation using Docusaurus swizzling to wrap DocItem/Layout with the new ChapterToolbar component. Reuses existing AgentBridge for API communication.

## Implementation Phases

### Phase 0: Research (Complete)
- Docusaurus swizzling approach for DocItem
- localStorage patterns for React
- Streaming content display patterns

### Phase 1: Design (Complete)
- Data model for user preferences
- API contract for Agent personalization/translation endpoints
- Component architecture

### Phase 2: Implementation (via /sp.tasks)
- Create ChapterToolbar component
- Implement useUserPreferences hook
- Swizzle DocItem/Layout
- Style with robotics theme
- Integration testing

## Complexity Tracking

> No violations - all gates pass. Simple implementation within existing architecture.

| Aspect | Complexity | Mitigation |
|--------|------------|------------|
| Docusaurus swizzling | Medium | Follow official swizzle patterns |
| Streaming content | Low | Reuse existing AgentBridge |
| RTL for Urdu | Medium | CSS dir="rtl" + proper font |
