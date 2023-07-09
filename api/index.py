import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler
from urllib import parse

def scrape_opengraph_metadata(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    og_properties = {}

    og_title_tag = soup.find("meta", property="og:title")
    if og_title_tag:
        og_properties["title"] = og_title_tag["content"]

    og_description_tag = soup.find("meta", property="og:description")
    if og_description_tag:
        og_properties["description"] = og_description_tag["content"]

    og_image_tag = soup.find("meta", property="og:image")
    if og_image_tag:
        og_properties["image"] = og_image_tag["content"]


    return og_properties

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = self.path.split("?")[1] if "?" in self.path else ""
        query_params = dict(parse.parse_qsl(parsed_url))

        if "url" in query_params:
            try:
                opengraph_data = scrape_opengraph_metadata(query_params["url"])
                response_message = str(opengraph_data)
            except Exception as e:
                response_message = "Error occurred while retrieving OpenGraph metadata: " + str(e)
        else:
            response_message = "Please provide a 'url' query parameter."

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode())
