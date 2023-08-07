import re


def parse_cooklang(cooklang_text):
    # extract ingredients with their quantities
    ingredients = re.findall(r"@([\w\s]+?){([\d/%\w\s]*?)}", cooklang_text)

    # extract tools
    tools = re.findall(r"#([\w\s]+?){([\d/%\w\s]*?)}", cooklang_text)

    # extract timers
    timers = re.findall(r"~{([\d/%\w\s]*?)}", cooklang_text)

    # extract metadata tags
    metadata = re.findall(r">> ([\w\s]+): ([\w\s.]+)", cooklang_text)

    return ingredients, tools, timers, metadata


def convert_to_markdown(cooklang_text, ingredients, tools, timers, metadata):
    # replace @ and {} with bold markdown for ingredients, remove quantities
    for ingredient, qty in ingredients:
        cooklang_text = cooklang_text.replace(
            f"@{ingredient}{{{qty}}}", f"**{ingredient}**"
        )

    # replace # and {} with italic markdown for tools
    for tool, qty in tools:
        cooklang_text = cooklang_text.replace(f"#{tool}{{{qty}}}", f"`{tool}`")

    # replace ~ with markdown for timers
    for timer in timers:
        cooklang_text = re.sub(
            f"~{{{timer}}}", f'*{timer.replace("%", " ")}*', cooklang_text
        )

    # add metadata tags as headers
    for tag, value in metadata:
        # cooklang_text = cooklang_text.replace(f'>> {tag}: {value}', f'### {tag}: {value}')
        # cooklang_text = cooklang_text.replace(f'>> {tag}: {value}\n', '')
        if tag == "title":
            title = value

    md = [f"# {title}"]
    for line in cooklang_text.split("\n"):
        if line.startswith(">"):
            continue
        elif line.strip():
            md.append(f"1. {line}")

    return "\n".join(md)
