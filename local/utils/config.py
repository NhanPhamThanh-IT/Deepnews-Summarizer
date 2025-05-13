import json

def load_config():
    """
    Load configuration data from a JSON file.

    Description:
    -----------
    This function reads and parses the contents of a file named `config.json`,
    which is expected to be located in the current working directory. The parsed
    data is returned as a Python dictionary.

    Behavior:
    --------
    - Opens the file `config.json` in read mode.
    - Parses the JSON content into a Python object (typically a dict).
    - Returns the configuration data for use in the application.

    Returns:
    -------
    dict
        The configuration data loaded from the JSON file.

    Raises:
    ------
    FileNotFoundError:
        If the `config.json` file does not exist.
    json.JSONDecodeError:
        If the file contains invalid JSON.

    Example:
    --------
    >>> config = load_config()
    >>> print(config["api_key"])
    """
    with open("config.json", "r") as f:
        config = json.load(f)
    return config
