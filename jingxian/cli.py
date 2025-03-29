# jingxian/cli.py

import sys
from jingxian.generator import build_site
from jingxian.server import serve
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: jingxian [build|serve] [site_path]")
        sys.exit(1)

    command = sys.argv[1]
    site_path = sys.argv[2] if len(sys.argv) > 2 else "."
    site_path = Path(site_path).resolve()
    print(site_path)

    if command == "build":
        build_site(site_path)
    elif command == "serve":
        serve(site_path)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)