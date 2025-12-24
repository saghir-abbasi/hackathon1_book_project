# Research: Personalization & Translation UI

**Feature**: 008-feature-personalization-translation
**Date**: 2025-12-22

## Research Areas

### 1. Docusaurus DocItem Swizzling

**Decision**: Use `@docusaurus/theme-classic` swizzling to wrap DocItem/Layout

**Rationale**:
- Docusaurus supports "swizzling" to customize theme components
- DocItem/Layout wraps the content of each documentation page
- Wrapping (not ejecting) allows us to add UI without breaking updates

**Alternatives Considered**:
- **MDX components**: Would require modifying each chapter file - rejected for maintenance burden
- **Global CSS injection**: Cannot add interactive React components - rejected
- **Plugin approach**: Over-engineered for simple UI addition - rejected

**Implementation**:
```bash
npm run swizzle @docusaurus/theme-classic DocItem/Layout -- --wrap
```

### 2. localStorage for User Preferences

**Decision**: Use localStorage with a custom React hook

**Rationale**:
- No backend changes required (per spec: "client-side context")
- Persists across page reloads (FR-002, SC-003)
- Simple, well-supported browser API

**Alternatives Considered**:
- **sessionStorage**: Would not persist across sessions - rejected
- **Cookies**: Unnecessary complexity for non-sensitive data - rejected
- **IndexedDB**: Over-engineered for simple key-value storage - rejected

**Data Structure**:
```typescript
interface UserPreferences {
  background: 'software' | 'hardware' | null;
  lastUpdated: string; // ISO date
}
```

### 3. Streaming Content Display

**Decision**: Reuse existing AgentBridge with content overlay

**Rationale**:
- AgentBridge already handles SSE streaming from `/api/agent/query`
- Can display streamed content in a dedicated overlay/panel
- Consistent with existing chatbot implementation

**Alternatives Considered**:
- **New API endpoint**: Unnecessary - existing agent can handle prompts - rejected
- **Batch response**: Worse UX than streaming - rejected

**Content Transformation Prompts**:

**Personalization (Software background)**:
```
You are adapting the following robotics content for a SOFTWARE developer audience.
Emphasize: code patterns, APIs, software architecture, debugging, testing.
Use analogies from: web development, databases, microservices, DevOps.

Original content:
{chapter_content}

Rewrite this content with software-focused explanations and analogies.
```

**Personalization (Hardware background)**:
```
You are adapting the following robotics content for a HARDWARE engineer audience.
Emphasize: circuits, sensors, actuators, electrical systems, mechanical design.
Use analogies from: electronics, embedded systems, control theory, manufacturing.

Original content:
{chapter_content}

Rewrite this content with hardware-focused explanations and analogies.
```

**Translation to Urdu**:
```
Translate the following robotics educational content to Urdu.
Maintain technical terms in English where no standard Urdu equivalent exists.
Ensure the translation is clear and educational.

Original content:
{chapter_content}

Provide the Urdu translation:
```

### 4. RTL Support for Urdu

**Decision**: Use CSS `dir="rtl"` with Noto Nastaliq Urdu font

**Rationale**:
- Urdu is a right-to-left (RTL) language
- Noto Nastaliq Urdu is a high-quality, free Google font
- CSS direction property handles layout automatically

**Implementation**:
```css
.urdu-content {
  direction: rtl;
  font-family: 'Noto Nastaliq Urdu', serif;
  font-size: 1.2em; /* Urdu script needs slightly larger size */
  line-height: 2; /* Better readability for Nastaliq */
}
```

### 5. UI/UX for Buttons

**Decision**: Floating toolbar at top of chapter content with neon/cyberpunk theme

**Rationale**:
- Matches existing robotics theme (UI-001)
- Clearly visible without obstructing content
- Accessible and mobile-friendly

**Button Design**:
- "Personalize" button with user icon
- "اردو میں ترجمہ" (Translate to Urdu) button with language icon
- Loading state with animated spinner
- Disabled state during processing

## Summary of Decisions

| Topic | Decision | Key Reason |
|-------|----------|------------|
| Component injection | DocItem swizzle wrap | Non-invasive, maintainable |
| Preference storage | localStorage hook | Simple, persists, no backend |
| Content streaming | Reuse AgentBridge | Consistent, already working |
| Urdu rendering | RTL CSS + Noto font | Proper script support |
| UI placement | Floating toolbar | Visible, non-obtrusive |
