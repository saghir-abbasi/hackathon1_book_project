import React, { useEffect, useState } from 'react';
import DOMPurify from 'dompurify';

const MAX_SELECTION_LENGTH = 1000; // As decided in the spec

export function useTextSelection() {
  const [selection, setSelection] = useState(null);

  useEffect(() => {
    const handleSelectionChange = () => {
      const currentSelection = window.getSelection();

      // Ensure actual text is selected
      if (currentSelection && currentSelection.type === 'Range' && currentSelection.toString().length > 0) {
        const range = currentSelection.getRangeAt(0);
        const commonAncestor = range.commonAncestorContainer;

        let currentElement = commonAncestor.nodeType === Node.TEXT_NODE ? commonAncestor.parentElement : commonAncestor;

        let chapterId = null;
        let sectionId = null;
        let startOffset = range.startOffset;
        let endOffset = range.endOffset;

        // Traverse up the DOM tree to find chapter (H1) and section (H2/H3) IDs
        while (currentElement && currentElement !== document.body) {
          if (currentElement.tagName.startsWith('H') && currentElement.id) {
            const level = parseInt(currentElement.tagName.substring(1), 10);

            if (level === 1 && !chapterId) {
              chapterId = currentElement.id;
            } else if ((level === 2 || level === 3) && !sectionId) {
              sectionId = currentElement.id;
            }

            if (chapterId && sectionId) {
              break;
            }
          }
          currentElement = currentElement.parentElement;
        }

        // Sanitize and limit selected text
        const rawSelectedText = currentSelection.toString();
        const sanitizedSelectedText = DOMPurify.sanitize(rawSelectedText, { USE_PROFILES: { html: false } });
        const limitedSelectedText = sanitizedSelectedText.substring(0, MAX_SELECTION_LENGTH);

        setSelection({
          selectedText: limitedSelectedText,
          chapterId: chapterId,
          sectionId: sectionId,
          offsets: [startOffset, endOffset],
        });
      } else {
        setSelection(null); // Clear selection if no text is selected
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange); // For keyboard selections

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
    };
  }, []);

  return selection;
}
