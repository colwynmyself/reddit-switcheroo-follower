from io import open


def write_links_to_csv(csv, links):
    with open(csv, 'w+') as f:
        depth = 0
        for text, link in links:
            f.write(f'"{text}",{link},{depth}\n')
            depth += 1