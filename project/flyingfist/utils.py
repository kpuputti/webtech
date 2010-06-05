def escape_html(s):
    escapes = (
        ('&', '&amp;'),
        ('"', '&quot;'),
        ("'", '&#39;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
    )
    escaped = s
    for ch, seq in escapes:
        escaped = escaped.replace(ch, seq)
    return escaped
