import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def download_all_images(query):
    image_links = set()

    # Searching for the query in Google Images
    search_query = query + " images"
    for j in search(search_query, num=10, stop=10, pause=2):
        if 'https://encrypted-tbn0.gstatic.com/images' in j:
            continue
        page = requests.get(j)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extracting image links
        for raw_img in soup.find_all("img"):
            link = raw_img.get("src")
            if link and link.startswith("http"):
                image_links.add(link)

    # Create a directory for downloaded images
    if not os.path.exists(query):
        os.makedirs(query)

    # Download the images
    for i, link in enumerate(image_links):
        try:
            response = requests.get(link)
            file = open(os.path.join(query, f"{query}_{i+1}.jpg"), "wb")
            file.write(response.content)
            file.close()
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print(f"Downloaded {len(image_links)} images for {query}.")
    return


query = "squirtle in game"  # Enter your search query

download_all_images(query)