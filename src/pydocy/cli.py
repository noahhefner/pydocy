import argparse
from pathlib import Path

from pydocy.walk_source import walk_source


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Path to process")

    args = parser.parse_args()

    result = walk_source(args.path, [])
    print(result)
