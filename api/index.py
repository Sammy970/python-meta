import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler
from urllib import parse

def scrape_opengraph_metadata(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    og_properties = {}
    meta_tags = soup.find_all("meta", property=lambda prop: prop.startswith("og:"))
    
    for tag in meta_tags:
        property_name = tag["property"][3:]
        property_value = tag["content"]
        og_properties[property_name] = property_value

    return og_properties

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = self.path.split("?")[1] if "?" in self.path else ""
        query_params = dict(parse.parse_qsl(parsed_url))

        if "url" in query_params:
            opengraph_data = scrape_opengraph_metadata(query_params["url"])
            response_message = str(opengraph_data)
        else:
            response_message = "Please provide a 'url' query parameter."

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode())
