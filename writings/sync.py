import glob
from pathlib import Path
import random
import os
import subprocess
import json
from datetime import datetime
import re
from pprint import pprint
import requests

import tabulate
from logzero import logger

IN_PATH = "/home/hfb/writings/inputs"
OUT_PATH = "/home/hfb/writings/posts"
CONTENT_PATH = "/home/hfb/complex.codes/content/posts"
GIST_REGEX = r"https:\/\/gist.githubusercontent.com\/[A-Za-z0-9]*\/[A-Za-z0-9]*\/raw\/[A-Za-z0-9]*\/[A-Za-z0-9]*\..[a-z]+"


def extract_path(raw_path):
    path = clean_raw_path(raw_path)
    safe_path = "".join(c for c in path if c.isalnum() or c == " ").replace("  ", " ")
    return safe_path.lower().replace(" ", "-")


def extract_title(raw_path):
    return clean_raw_path(raw_path)


def clean_raw_path(raw_path):
    return ".".join(Path(raw_path).name.split(".")[:-1])


def open_config(local_path, title=None):
    config_path = f"{local_path}/config.json"
    config = {}
    try:
        with open(config_path, "r") as f:
            config = json.loads(f.read())
            logger.debug("Using existing configuration...")
    except FileNotFoundError:
        print("No config found...")
    finally:
        if not config:
            config = build_config(config, title=title)
        with open(config_path, "w+") as f:
            f.write(json.dumps(config))
        return config


def build_config(config, title=None):
    return {
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "description": "",
        "views": random.randint(0, 1000),
    }


def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError as e:
        pass


def sync():
    logger.info("Syncing writings...")
    writings = [["Header", "URL", "Updated"]]
    subprocess.run(f"rm -r {CONTENT_PATH}".split())
    for raw_path in glob.glob(f"{IN_PATH}/*"):
        logger.info(f"Processing {raw_path}")
        path = extract_path(raw_path)
        title = extract_title(raw_path)
        local_path = f"{OUT_PATH}/{path}"
        mkdir(local_path)
        subprocess.run(
            [
                "pandoc",
                "-s",
                raw_path,
                "-t",
                "gfm",
                "-o",
                f"{local_path}/raw.md",
            ]
        )
        config = open_config(local_path, title=title)
        writings.append([title, path, False])

        with open(f"{local_path}/index.md", "w+") as f:
            f.write("---\n")
            for key, value in config.items():
                f.write(f"{key}: {json.dumps(value)}\n")
            f.write("---\n")
            with open(f"{local_path}/raw.md") as inp:
                for line in inp:
                    if re.search(GIST_REGEX, line):
                        match = re.search(GIST_REGEX, line).group(0)
                        print(match)
                        code = requests.get(match).text
                        language = match.split(".")[-1]
                        f.write(f"```{language}\n")
                        for line in code:
                            f.write(line)
                        f.write(f"\n```\n")
                    else:
                        f.write(line.replace("\\", ""))

        content_path = f"{CONTENT_PATH}/{path}"
        mkdir(CONTENT_PATH)
        mkdir(content_path)
        with open(f"{local_path}/index.md", "r") as inp:
            with open(f"{content_path}/index.md", "w+") as out:
                out.write(inp.read())

    print(tabulate.tabulate(writings, headers="firstrow"))

def main():
    sync()


if __name__ == "__main__":
    main()
