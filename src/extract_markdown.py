import re

def extract_markdown_images(text):
    images = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        name = match[0]
        url = match[1]
        image = name, url
        images.append(image)
    return images
    
def extract_markdown_links(text):
    links = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        name = match[0]
        url = match[1]
        link = name, url
        links.append(link)
    return links





