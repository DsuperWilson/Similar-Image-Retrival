import requests


API_KEY = 'AIzaSyDaDX7eSr48qakxAKcTS-0FjcZ-HGnPVjs'
CX = 'd48e4209732304921'

# Install google_images_search library using pip: pip install google_images_search
from google_images_search import GoogleImagesSearch

# Define Google Images API credentials
gis = GoogleImagesSearch(API_KEY, CX)

# Define search function
def search_images(query):
    # Define search parameters
    _search_params = {
        'q': query,  # Search query
        'num': 10,  # Number of search results
        'imgSize': 'large',  # Size of images to search for
        'imgType': 'photo',  # Type of images to search for
        'safe': 'medium',  # Safe search level
        'fileType': 'jpg|png',  # File types to search for
    }

    # Execute search
    gis.search(search_params=_search_params)

    # Print URLs of search results

    count = 1
    for image in gis.results():
        response = requests.get(image.url)
        if response.status_code == 200:
            with open('images/'+str(query)+str(count)+'.jpg', 'wb') as f:
                f.write(response.content)
            count += 1
        else:
            print("Failed to download the image. Status code:", response.status_code)

# Call search function with user input query

def main():
    search_images('Ironman')

if __name__ == '__main__':
    main()