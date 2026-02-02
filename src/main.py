import os
import shutil
import sys

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


def generate_page(from_path, template_path, dest_path, base_path):
    print(
        f"Generating page from {from_path} to {dest_path} using template: {template_path}"
    )
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    full_html_page = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
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


def generate_pages_recursive(from_path, template_path, dest_path, base_path):
    if os.path.isfile(from_path):
        des_path = os.path.join(
            os.path.dirname(dest_path),
            os.path.basename(from_path).replace(".md", ".html"),
        )
        generate_page(from_path, template_path, des_path, base_path)
    elif os.path.isdir(from_path):
        for item in os.listdir(from_path):
            generate_pages_recursive(
                os.path.join(from_path, item),
                template_path,
                os.path.join(dest_path, item),
                base_path,
            )


def main():
    base_path = "/"
    if len(sys.argv) == 2:
        base_path = sys.argv[1]

    copy_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)


main()
