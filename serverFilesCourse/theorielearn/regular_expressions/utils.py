def convert_regex_to_latex(submitted_re: str) -> str:
    """Convert submitted_re to latex formatted regex."""
    return submitted_re.replace("e", "\\epsilon").replace("*", "^*")
