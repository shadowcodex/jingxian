from livereload import Server
from jingxian.generator import build_site
from pathlib import Path

def serve(site_path):
    build_site(site_path)

    print("Serving at http://127.0.0.1:4000 (Live reload enabled)")
    server = Server()

    watch_dirs = [
        '_content',
        '_templates',
        '_data',
        '_datapages',
        '_collections'
    ]

    for folder in watch_dirs:
        glob_path = str(site_path / folder / '**' / '*')
        print(f"Watching: {glob_path}")
        server.watch(glob_path, lambda: print(f"🔁 Change detected in {folder}") or build_site(site_path))

    server.serve(root=str(site_path / 'build'), host='127.0.0.1', port=4000)
