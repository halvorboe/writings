import glob
import random
import os
import subprocess
import json
from datetime import datetime

import tabulate

IN_PATH = "/home/dev/writings"
OUT_PATH = "/home/dev/projects/writings/posts"
CONTENT_PATH = "/home/dev/projects/complex.codes/html/content/posts"

def extract_path(raw_path):
    path = clean_raw_path(raw_path)
    safe_path = "".join(c for c in path if c.isalnum() or c == " ").replace("  ", " ")
    return safe_path.lower().replace(" ", "-")

def extract_title(raw_path):
    return clean_raw_path(raw_path)

def clean_raw_path(raw_path):
    return raw_path.split("/")[-1].strip(".edited.docx")

def open_config(local_path, title=None):
    config_path = f"{local_path}/config.json"
    config = {}
    try:
        with open(config_path, "r") as f:
            config = json.loads(f.read())
            print("Using existing configuration...")
    except FileNotFoundError:
        print("No config found...")
    finally:
        final_config = build_config(config, title=title)
        with open(config_path, "w+") as f:
            f.write(json.dumps(final_config)) 
        return final_config

def build_config(config, title=None):
    return {
        "title": title,
        "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "description": "",
        "views": random.randint(0, 1000),
        "draft": False,
        # "draft": input("Is it a draft? [y/n]") == "y",
    }

def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError as e:
        pass


def main():
    print("Syncing writings...")
    writings = [["Header", "URL", "Updated"]]
    for raw_path in glob.glob(f"{IN_PATH}/*"):
        path = extract_path(raw_path)
        title = extract_title(raw_path)
        local_path = f"{OUT_PATH}/{path}"
        mkdir(local_path)
        subprocess.run(["pandoc", "-s", raw_path, "-t", "markdown", "-o", f"{local_path}/raw.md"])
        config = open_config(local_path, title=title)
        writings.append([title, path, False])
        content_path = f"{CONTENT_PATH}/{path}"
        mkdir(content_path)
        with open(f"{content_path}/index.md", "w+") as f:
            f.write("---\n")
            for key, value in config.items():
                f.write(f"{key}: {json.dumps(value)}\n")
            f.write("---\n")
            with open(f"{local_path}/raw.md") as inp:
                for line in inp:
                    f.write(line)
        

    print(tabulate.tabulate(writings, headers="firstrow"))

if __name__ == "__main__":
    main()
