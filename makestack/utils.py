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


def append_to_file_top(file_path, content):
    with open(file_path, "r+") as file:
        content = str(content) + file.read()
        file.seek(0, 0)
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


def verify_requirement(requirement_path, requirement):
    with open(requirement_path, "r") as file:
        for line in file:
            if requirement in line:
                return True
        return False


def add_requirement(requirement_path, requirement):
    if not verify_requirement(requirement_path, requirement):
        append_to_file(requirement_path, requirement)


def verify_import(file_path, import_string):
    with open(file_path, "r") as file:
        for line in file:
            if import_string in line:
                return True
        return False


def add_native_import(file_path, import_string):
    if not verify_import(file_path, import_string):
        append_to_file_after_matching(
            file_path,
            "# Native Libraries Imports",
            import_string,
        )


def add_third_party_import(file_path, import_string):
    if not verify_import(file_path, import_string):
        append_to_file_after_matching(
            file_path,
            "# Third Party Libraries Imports",
            import_string,
        )


def add_local_import(file_path, import_string):
    if not verify_import(file_path, import_string):
        append_to_file_after_matching(
            file_path,
            "# Local Libraries Imports",
            import_string,
        )
