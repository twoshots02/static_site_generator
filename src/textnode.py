from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINKS = "Links"
    IMAGES = "Images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __str__(self):
        return f"{self.text} ({self.text_type})"
    
    def __repr__(self):
        return f"{self.text} ({self.text_type})"
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url