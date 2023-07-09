import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler
from urllib import parse

def scrape_opengraph_metadata(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract OpenGraph metadata
    og_title = soup.find("meta", property="og:title")["content"]
    og_description = soup.find("meta", property="og:description")["content"]
    og_image = soup.find("meta", property="og:image")["content"]
    # ...

    return {
        "title": og_title,
        "description": og_description,
        "image": og_image,
        # Include additional metadata as needed
    }

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = parse.urlsplit(self.path)
        query_params = dict(parse.parse_qsl(parsed_url.query))

        if "url" in query_params:
            opengraph_data = scrape_opengraph_metadata(query_params["url"])
            response_message = str(opengraph_data)
        else:
            response_message = "Please provide a 'url' query parameter."

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode())

    from http.server import HTTPServer
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()
