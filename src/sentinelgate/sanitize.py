# import re

# _GREETING_PREFIX_RE = re.compile(
#     r"""^\s*(
#         hey|hi|hello|yo|hii|hiii|heyy|heyya|good\s+morning|good\s+afternoon|good\s+evening
#     )\b[\s,!.\-]*""",
#     re.IGNORECASE | re.VERBOSE,
# )

# _FILLER_PREFIX_RE = re.compile(
#     r"""^\s*(
#         pls|plz|please|kindly|quick\s+question|one\s+question|just\s+checking
#     )\b[\s,:;!.\-]*""",
#     re.IGNORECASE | re.VERBOSE,
# )

# def sanitize_prompt(prompt: str) -> str:
#     """
#     Removes common greeting/filler prefixes without changing meaning.
#     Only trims prefixes (safe): does NOT delete content in the middle.
#     """
#     if not prompt:
#         return prompt

#     s = prompt.strip()

#     # Remove greeting/filler prefixes a few times (handles "hey, hi, please ...")
#     for _ in range(3):
#         before = s
#         s = _GREETING_PREFIX_RE.sub("", s).lstrip()
#         s = _FILLER_PREFIX_RE.sub("", s).lstrip()
#         if s == before:
#             break

#     # Normalize whitespace
#     s = re.sub(r"\s+", " ", s).strip()

#     # If we stripped everything by accident, fall back to original
#     return s if s else prompt.strip()


# import re

# _GREETING_PREFIX_RE = re.compile(
#     r"""^\s*(
#         hey|hi|hello|yo|hii|hiii|heyy|heyya|good\s+morning|good\s+afternoon|good\s+evening
#     )\b[\s,!.\-]*""",
#     re.IGNORECASE | re.VERBOSE,
# )

# _FILLER_PREFIX_RE = re.compile(
#     r"""^\s*(
#         pls|plz|please|kindly|quick\s+question|one\s+question|just\s+checking
#     )\b[\s,:;!.\-]*""",
#     re.IGNORECASE | re.VERBOSE,
# )

# def sanitize_prompt(prompt: str) -> str:
#     if not prompt:
#         return prompt

#     s = prompt.strip()

#     for _ in range(3):
#         before = s
#         s = _GREETING_PREFIX_RE.sub("", s).lstrip()
#         s = _FILLER_PREFIX_RE.sub("", s).lstrip()
#         if s == before:
#             break

#     s = re.sub(r"\s+", " ", s).strip()
#     return s if s else prompt.strip()


import re

_GREETING_PREFIX_RE = re.compile(
    r"""^\s*(
        hey|hi|hello|yo|hii|hiii|heyy|heyya|
        good\s+morning|good\s+afternoon|good\s+evening
    )\b[\s,!.\-]*""",
    re.IGNORECASE | re.VERBOSE,
)

_FILLER_PREFIX_RE = re.compile(
    r"""^\s*(
        pls|plz|please|kindly|quick\s+question|one\s+question|just\s+checking
    )\b[\s,:;!.\-]*""",
    re.IGNORECASE | re.VERBOSE,
)

# ✅ NEW: short ack/filler prefixes that hurt classification if left in front
_ACK_PREFIX_RE = re.compile(
    r"""^\s*(
        ok|okay|k|kk|test|thanks|thank\s+you
    )\b[\s,:;!.\-]*""",
    re.IGNORECASE | re.VERBOSE,
)

def sanitize_prompt(prompt: str) -> str:
    """
    Remove greeting/filler prefixes only (start of string), repeatedly.
    Example:
      "hi hey ok, shipment status" -> "shipment status"
    """
    if prompt is None:
        return ""

    s = str(prompt).strip()
    if not s:
        return ""

    # Remove up to N prefix tokens in a row
    for _ in range(10):
        before = s
        s = _GREETING_PREFIX_RE.sub("", s).lstrip()
        s = _FILLER_PREFIX_RE.sub("", s).lstrip()
        s = _ACK_PREFIX_RE.sub("", s).lstrip()
        if s == before:
            break

    # Normalize whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # If everything was removed, return empty string
    return s
