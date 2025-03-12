# server.py
from livereload import Server
from generator import build_site

def serve():
    # Initial build
    build_site()
    print("Serving at http://127.0.0.1:4000 (Live reload enabled)")
    # Create a livereload server
    server = Server()
    # Watch relevant folders for changes, triggering rebuild on any change
    server.watch('content/*', build_site)
    server.watch('templates/*', build_site)
    server.watch('data/*', build_site)
    server.watch('collections/*', build_site)
    server.watch('static/*', build_site)
    # Serve the output directory on port 4000
    server.serve(root='output', host='127.0.0.1', port=4000)
