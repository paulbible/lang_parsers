"""
    A set of reusable utilities for parsing languages.
"""
import re


def comment_remover_cpp(text):
    """
    https://stackoverflow.com/questions/57208950/how-to-get-only-function-blocks-using-sly
    :param text:
    :return:
    """
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)
