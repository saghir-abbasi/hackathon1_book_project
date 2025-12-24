# Quickstart: Personalization & Translation UI

**Feature**: 008-feature-personalization-translation
**Date**: 2025-12-22

## Prerequisites

- Node.js 18+ installed
- Docusaurus site running locally (`npm start`)
- Backend API running (for Agent endpoint)

## Quick Setup

### 1. Install Dependencies

No new dependencies required - uses existing React and Docusaurus packages.

### 2. Swizzle DocItem Layout

```bash
cd docusaurus-book-site
npm run swizzle @docusaurus/theme-classic DocItem/Layout -- --wrap --typescript
```

This creates: `src/theme/DocItem/Layout/index.tsx`

### 3. Create Components

Create the following files:

```
src/
├── components/
│   └── ChapterToolbar/
│       ├── index.tsx
│       ├── PersonalizeButton.tsx
│       ├── TranslateButton.tsx
│       ├── ContentOverlay.tsx
│       ├── BackgroundModal.tsx
│       └── styles.module.css
│
└── hooks/
    └── useUserPreferences.ts
```

### 4. Add Urdu Font

Add to `docusaurus.config.ts`:

```typescript
headTags: [
  {
    tagName: 'link',
    attributes: {
      rel: 'stylesheet',
      href: 'https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap',
    },
  },
],
```

### 5. Test Locally

```bash
npm start
```

Navigate to any chapter page and verify:
- [ ] Personalize button appears at top
- [ ] Translate button appears at top
- [ ] Clicking Personalize shows modal (first time)
- [ ] Clicking Translate starts streaming Urdu content

## Development Commands

```bash
# Start development server
cd docusaurus-book-site
npm start

# Build for production
npm run build

# Test build locally
npm run serve
```

## Testing Checklist

### Personalization Flow

1. [ ] Open a chapter page
2. [ ] Click "Personalize" button
3. [ ] Verify modal appears asking for background
4. [ ] Select "Software" and confirm
5. [ ] Verify content starts streaming
6. [ ] Verify overlay shows personalized content
7. [ ] Close overlay, click Personalize again
8. [ ] Verify it triggers immediately (no modal)
9. [ ] Refresh page, click Personalize
10. [ ] Verify preference persists (no modal)

### Translation Flow

1. [ ] Open a chapter page
2. [ ] Click "اردو میں ترجمہ" button
3. [ ] Verify loading state appears
4. [ ] Verify Urdu content streams in RTL
5. [ ] Verify technical terms remain in English
6. [ ] Close overlay

### Edge Cases

1. [ ] Test with long chapter content
2. [ ] Test offline behavior (graceful error)
3. [ ] Test on mobile viewport
4. [ ] Test keyboard navigation (accessibility)

## File Structure After Implementation

```
docusaurus-book-site/
├── src/
│   ├── components/
│   │   ├── ChapterToolbar/
│   │   │   ├── index.tsx
│   │   │   ├── PersonalizeButton.tsx
│   │   │   ├── TranslateButton.tsx
│   │   │   ├── ContentOverlay.tsx
│   │   │   ├── BackgroundModal.tsx
│   │   │   └── styles.module.css
│   │   └── ... (existing components)
│   │
│   ├── hooks/
│   │   └── useUserPreferences.ts
│   │
│   ├── theme/
│   │   └── DocItem/
│   │       └── Layout/
│   │           └── index.tsx  (swizzled)
│   │
│   └── agent-client/
│       └── agentBridge.js  (existing, reused)
│
└── docusaurus.config.ts  (updated with font)
```

## Troubleshooting

### "ChapterToolbar not showing"

1. Check that DocItem/Layout was properly swizzled
2. Verify the swizzled component imports ChapterToolbar
3. Check browser console for errors

### "Agent API not responding"

1. Ensure backend is running on correct port
2. Check CORS configuration includes localhost
3. Verify API_BASE_URL in agent-client config

### "Urdu text not displaying correctly"

1. Verify Noto Nastaliq Urdu font is loaded
2. Check that RTL CSS is applied to overlay
3. Test with different browsers

### "Preference not persisting"

1. Check localStorage in browser DevTools
2. Verify key is `book_user_preferences`
3. Check for localStorage quota errors
