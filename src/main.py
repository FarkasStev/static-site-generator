import os
import shutil

from markdown_to_html import markdown_to_html_node


def copy_files(source_dir, destination_dir):
    # Implement file copying logic here
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    for contents in os.listdir(source_dir):
        if os.path.isfile(contents):
            print(f"Copying file: {contents}")
            shutil.copy(contents, destination_dir)
        elif os.path.isdir(contents):
            print(f"Copying directory: {contents}")
            copy_files(contents, os.path.join(destination_dir, contents))


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using template: {template_path}"
    )

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    full_html_page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(full_html_page)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")


def main():
    copy_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
