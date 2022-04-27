"""Tools for internationalization."""
from configparser import ConfigParser
from os import path


def i18n(category: str, key: str):
    """
    Internationalize a string that does not take any formatting.

    Parameters
    ----------
    category: str
        The string category in the strings.properties file.
    key: str
        The string key in the strings.properties file.

    Returns
    -------
    The internationalized string.
    """
    parser = ConfigParser()
    parser.read(path.join(path.dirname(__file__), "strings.properties"))
    msg: str = parser.get(category, key)
    return msg
