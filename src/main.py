import os
import shutil

from textnode import TextNode, TextType


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


def main():
    copy_files("static", "public")


main()
