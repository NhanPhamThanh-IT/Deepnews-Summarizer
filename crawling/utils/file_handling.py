def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)