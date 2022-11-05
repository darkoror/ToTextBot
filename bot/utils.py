def normalize_text(msg: str):
    """
    Removes redundant spaces between words (removes all and then put only 1 between words)
    :param msg: any text message
    :return: text without redundant spaces
    """
    msg_rows = msg.split('\n')
    normalized_rows = []
    for row in msg_rows:
        if row.replace(' ', '') != '':
            normalized_rows.append(' '.join(row.split()))  # split() - removes all spaces

    return '\n'.join(normalized_rows)

