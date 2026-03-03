#!/usr/bin/env python3
"""
Standalone external grader for CFG writing questions.
No NLTK dependency — uses plain Python data structures.

Algorithm: fixed-point per-nonterminal string-set iteration.
For each nonterminal NT we compute lang[NT] = set of strings
derivable from NT up to MAX_LENGTH_TO_CHECK, iterating until
no new strings are added.  This is faster and more correct than
sentential-form BFS (no "+3 buffer" needed, no tuple-explosion
for S->SS-style productions).
"""

import json
import os
import sys

sys.path.insert(0, "/grade/tests")

MAX_LENGTH_TO_CHECK = 14

# If any single nonterminal generates more strings than this the grammar
# almost certainly generates non-target strings; we cap and report early.
_MAX_LANG_SIZE = 5000

_EPSILON_KEYWORDS = {"e", "eps", "epsilon", "ε"}


# ---------------------------------------------------------------------------
# Nonterminal type: just a str subclass so isinstance() distinguishes it
# from terminal characters without any NLTK overhead.
# ---------------------------------------------------------------------------
class NT(str):
    __slots__ = ()


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _tokenize_alt(text):
    """
    Tokenize one RHS alternative into a list of NT/str symbols,
    or return None to indicate epsilon.
    """
    stripped = text.strip()
    if not stripped or stripped.lower() in _EPSILON_KEYWORDS:
        return None  # epsilon

    rhs = []
    i = 0
    while i < len(stripped):
        c = stripped[i]
        if c in " \t":
            i += 1
        elif c.isupper():
            # Nonterminal: uppercase letter followed by lowercase letters, digits, or underscore.
            # An uppercase letter always starts a NEW nonterminal, so "SS" → S, S and "AB" → A, B.
            j = i + 1
            while j < len(stripped) and (stripped[j].islower() or stripped[j] == "_"):
                j += 1
            rhs.append(NT(stripped[i:j]))
            i = j
        elif c.isdigit():
            rhs.append(c)  # plain str terminal
            i += 1
        elif c.islower():
            # Lowercase run → terminal characters (e.g. "ban", "ill", "ini")
            # Note: a standalone alternative of just "e"/"eps"/"epsilon" is
            # already handled above as epsilon before we reach this loop.
            j = i + 1
            while j < len(stripped) and stripped[j].islower():
                j += 1
            for ch in stripped[i:j]:
                rhs.append(ch)
            i = j
        elif c in ("'", '"'):
            end = stripped.index(c, i + 1)
            for ch in stripped[i + 1 : end]:
                rhs.append(ch)
            i = end + 1
        else:
            raise ValueError(
                f"Unexpected character {c!r} in alternative {text!r}. "
                "Nonterminals must start with an uppercase letter; "
                "terminals are lowercase letters or digits; use 'e' for epsilon."
            )
    return rhs


def parse_grammar(text):
    """
    Parse natural CFG notation.
    Returns (start: NT, prods: dict[NT, list[tuple]]).
    Each production RHS is a tuple of NT | str items; epsilon = empty tuple.
    """
    prods = {}
    start = None

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "→" in line:
            lhs_str, rhs_str = line.split("→", 1)
        elif "->" in line:
            lhs_str, rhs_str = line.split("->", 1)
        else:
            raise ValueError(f"Rule missing '->': {line!r}")

        lhs_str = lhs_str.strip()
        if not lhs_str:
            raise ValueError(f"Missing nonterminal in: {line!r}")
        lhs = NT(lhs_str)

        if start is None:
            start = lhs
        prods.setdefault(lhs, [])

        for alt in rhs_str.split("|"):
            rhs = _tokenize_alt(alt)
            prods[lhs].append(tuple(rhs) if rhs is not None else ())

    if not prods:
        raise ValueError("No grammar rules found.")
    return start, prods


# ---------------------------------------------------------------------------
# Language generation
# ---------------------------------------------------------------------------

def _expand_rhs(rhs, lang_by_len, max_len):
    """
    Return the set of all strings derivable from one production RHS,
    up to max_len characters.  Builds the set incrementally symbol by symbol.

    lang_by_len maps NT → dict[length → list[str]] for fast length-filtered
    cross-products.  This avoids the O(n²) blow-up when a nonterminal like S
    appears in S→SS and the language of S is large: instead of trying every
    pair (s, t) and filtering, we only iterate over length buckets that can
    actually fit within max_len.
    """
    current = {""}
    for sym in rhs:
        if not current:
            break
        if isinstance(sym, NT):
            ext_by_len = lang_by_len.get(sym)
            if not ext_by_len:
                current = set()
                break
            new_current = set()
            for s in current:
                remain = max_len - len(s)
                for l in range(remain + 1):
                    for t in ext_by_len.get(l, ()):
                        new_current.add(s + t)
            current = new_current
        else:
            # Terminal character
            current = {s + sym for s in current if len(s) < max_len}
    return current


def generate_language(start, prods, max_len):
    """
    Compute {strings derivable from start} ∩ Σ^{≤max_len}.

    Runs fixed-point iteration: for each nonterminal, expand all its
    productions using currently-known strings for other nonterminals,
    and repeat until nothing new is added.

    Returns (language_set, overflowed: bool).
    overflowed=True means some nonterminal hit _MAX_LANG_SIZE — the
    grammar almost certainly generates strings outside the target language.
    """
    lang = {nt: set() for nt in prods}
    # Length-indexed view of lang, kept in sync, for efficient cross-products.
    lang_by_len = {nt: {} for nt in prods}
    overflowed = False

    def _add_strings(nt, strings):
        """Add strings to lang[nt] and update lang_by_len[nt]."""
        lang[nt] |= strings
        lbl = lang_by_len[nt]
        for s in strings:
            l = len(s)
            if l not in lbl:
                lbl[l] = []
            lbl[l].append(s)

    changed = True
    while changed:
        changed = False
        for nt, productions in prods.items():
            if lang[nt] is None:
                continue
            for rhs in productions:
                new_strings = _expand_rhs(rhs, lang_by_len, max_len)
                added = new_strings - lang[nt]
                if added:
                    _add_strings(nt, added)
                    changed = True
                    if len(lang[nt]) > _MAX_LANG_SIZE:
                        lang[nt] = None  # sentinel: overflowed
                        lang_by_len[nt] = {}
                        overflowed = True
                        changed = True
                        break
            # If this NT just overflowed, don't process its remaining rules
            if lang[nt] is None:
                break

    result = lang.get(start)
    return (result if result is not None else set()), overflowed


# ---------------------------------------------------------------------------
# Grader entry point
# ---------------------------------------------------------------------------

def main():
    os.makedirs("/grade/results", exist_ok=True)

    try:
        with open("/grade/student/grammar.txt") as f:
            grammar_text = f.read()
    except FileNotFoundError:
        _write({"succeeded": False, "score": 0, "message": "No submission found."})
        return

    try:
        start, prods = parse_grammar(grammar_text)
    except Exception as e:
        _write({"succeeded": False, "score": 0, "message": f"Could not parse your grammar: {e}"})
        return

    try:
        from language_definition import generateLanguage
        try:
            from language_definition import MAX_LEN_OVERRIDE as _override
            effective_max = _override
        except ImportError:
            effective_max = MAX_LENGTH_TO_CHECK

        student_L, overflowed = generate_language(start, prods, effective_max)
        correct_L = generateLanguage(effective_max)

        false_positives = student_L - correct_L
        false_negatives = correct_L - student_L

        if false_positives:
            bad = min(false_positives, key=lambda s: (len(s), s))
            result = {"succeeded": True, "score": 0,
                      "message": f"Your grammar generates '{bad}', which is not in the language."}
        elif false_negatives:
            missing = min(false_negatives, key=lambda s: (len(s), s))
            result = {"succeeded": True, "score": 0,
                      "message": f"Your grammar does not generate '{missing}', which should be in the language."}
        elif overflowed:
            # No false positives detected in the strings we did check, but the
            # grammar generates far more strings than expected — likely wrong.
            result = {"succeeded": True, "score": 0,
                      "message": "Your grammar generates too many strings — check that it only generates the target language."}
        else:
            result = {"succeeded": True, "score": 1, "message": "Correct!"}

    except Exception as e:
        result = {"succeeded": False, "score": 0, "message": f"Grading error: {e}"}

    _write(result)


def _write(result):
    with open("/grade/results/results.json", "w") as f:
        json.dump(result, f)


if __name__ == "__main__":
    main()
