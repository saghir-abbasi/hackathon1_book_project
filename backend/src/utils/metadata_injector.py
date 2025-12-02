import bleach
from typing import List, Optional

class MetadataInjector:
    def __init__(self, max_selected_text_length: int = 1000):
        self.max_selected_text_length = max_selected_text_length
        # Define allowed HTML tags and attributes for bleach
        # Since we want to strip HTML, we don't allow any tags by default,
        # but bleach requires it to be an iterable.
        self.allowed_tags = []
        self.allowed_attributes = {}
        self.allowed_styles = []

    def sanitize_selected_text(self, text: str) -> str:
        """
        Sanitizes the selected text by stripping HTML tags and limiting length.
        """
        if not text:
            return ""
        
        # Strip all HTML tags
        sanitized_text = bleach.clean(
            text,
            tags=self.allowed_tags,
            attributes=self.allowed_attributes,
            styles=self.allowed_styles,
            strip=True # Strip disallowed tags/attributes
        )
        
        # Limit length
        return sanitized_text[:self.max_selected_text_length]

    def validate_offsets(self, offsets: Optional[List[int]]) -> bool:
        """
        Validates if offsets are a list of two non-negative integers.
        """
        if offsets is None:
            return True
        if not isinstance(offsets, list) or len(offsets) != 2:
            return False
        if not all(isinstance(o, int) and o >= 0 for o in offsets):
            return False
        return True

    def process_metadata(self, 
                         selected_text: Optional[str],
                         chapter_id: Optional[str],
                         section_id: Optional[str],
                         offsets: Optional[List[int]]) -> dict:
        """
        Validates and sanitizes incoming metadata.
        Returns a dictionary of processed metadata.
        """
        processed_data = {}

        if selected_text:
            processed_data["selected_text"] = self.sanitize_selected_text(selected_text)
        
        if chapter_id and isinstance(chapter_id, str):
            processed_data["chapter_id"] = chapter_id
            
        if section_id and isinstance(section_id, str):
            processed_data["section_id"] = section_id
            
        if self.validate_offsets(offsets):
            processed_data["offsets"] = offsets
        else:
            # Log a warning or handle invalid offsets as appropriate
            print(f"Warning: Invalid offsets received: {offsets}. Ignoring.")

        return processed_data

# Example Usage:
# injector = MetadataInjector(max_selected_text_length=1000)
# clean_data = injector.process_metadata(
#     selected_text="<p>Hello <script>alert('xss')</script> World!</p>",
#     chapter_id="intro-chapter",
#     section_id="first-section",
#     offsets=[0, 100]
# )
# print(clean_data)
