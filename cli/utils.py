import fileinput
import os
import re
import sys

import click
import qprompt


@qprompt.status("Creating the project folder.")
def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    else:
        raise click.ClickException(f"Directory {directory_path} already exists.")


def append_to_file(file_path, content):
    with open(file_path, "a") as file:
        file.write(content)


def append_to_file_after_matching(
    file_name, pattern, value, break_line_before=0, break_line_after=0
):
    fh = fileinput.input(file_name, inplace=True)

    for line in fh:
        before_breaks = "".join(["\n" for i in range(break_line_before)])
        after_breaks = "".join(["\n" for i in range(break_line_after)])
        replacement = line + before_breaks + value + after_breaks

        line = re.sub(pattern, replacement, line)
        sys.stdout.write(line)

    fh.close()


def replace_text_on_file(file_name, pattern, value):
    fh = fileinput.input(file_name, inplace=True)

    for line in fh:
        line = re.sub(pattern, value, line)
        sys.stdout.write(line)

    fh.close()


def create_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def get_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()


def copy_file(source, destination):
    with open(source, "r") as source_file:
        with open(destination, "w") as destination_file:
            destination_file.write(source_file.read())
