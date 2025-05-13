def save_file(filepath, content):
    """
    Save text content to a file.

    Description:
    -----------
    This function writes the given text content to a file at the specified path.
    If the file already exists, it will be overwritten. The content is saved using UTF-8 encoding.

    Parameters:
    ----------
    filepath : str
        The path (including filename) where the content should be saved.
    content : str
        The textual content to write into the file.

    Behavior:
    --------
    - Opens the target file in write mode (`'w'`), creating it if it doesn't exist.
    - Writes the provided content into the file using UTF-8 encoding.
    - Overwrites any existing content in the file.

    Raises:
    ------
    IOError:
        If the file cannot be written due to permissions or disk issues.

    Example:
    --------
    >>> save_file("output.txt", "This is a test.")
    # The file 'output.txt' will contain the text: This is a test.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
