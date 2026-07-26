import html
import re
import bleach
from bleach.css_sanitizer import CSSSanitizer


css_sanitizer = CSSSanitizer()

ALLOWED_TAGS = [
    'a', 'b', 'blockquote', 'br', 'em', 'i', 'u',
    'li', 'ol', 'p', 'strong', 'ul',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'pre', 'code', 'img', 'span'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
}


def clean_html(content):
    """
    Sanitizes HTML content before saving.
    Removes dangerous tags including their content.
    """

    if not content:
        return content

    # 1. Escaped HTML zurück in echtes HTML umwandeln
    content = html.unescape(content)

    # 2. Gefährliche komplette Blöcke entfernen
    content = re.sub(
        r'<(script|style|iframe|object|embed).*?>.*?</\1>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 3. Inline Event Handler entfernen (onerror, onclick, ...)
    content = re.sub(
        r'\s+on\w+\s*=\s*([\'"]).*?\1',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 4. Javascript URLs entfernen
    content = re.sub(
        r'javascript:',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 5. Bleach als letzte Schutzschicht
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        css_sanitizer=css_sanitizer
    )