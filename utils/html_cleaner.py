import bleach
from bleach.css_sanitizer import CSSSanitizer


css_sanitizer = CSSSanitizer()

ALLOWED_TAGS = [
    'a', 'b', 'blockquote', 'br', 'em', 'i', 'li', 'ol', 'p', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'pre', 'code', 'img', 'span'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],  # allow class and style on any tag
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
}


def clean_html(content):
    """Cleans the HTML content using bleach and returns cleaned content before saving."""
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        # css_sanitizer=css_sanitizer
    )
