import requests
from bs4 import BeautifulSoup

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

def main():
    url = "https://www.udemy.com/course/react-the-complete-guide-incl-redux"
    opengraph_data = scrape_opengraph_metadata(url)
    print(opengraph_data)

if __name__ == "__main__":
    main()
