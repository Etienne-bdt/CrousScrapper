import requests
from bs4 import BeautifulSoup

# Define the URL pattern
base_url = "https://infos-nutrition.crous-toulouse.fr/produit/"
start_i = 250
end_i = 2504

# Variables to store the count
count = 0
total = 0

# File to store URLs that result in a 404 error
error_file_path = "error_urls.txt"

# Set to store URLs with 404 errors
error_urls = set()

# Load previously saved error URLs
try:
    with open(error_file_path, 'r') as file:
        error_urls = set(map(int, file.read().splitlines()))
except FileNotFoundError:
    pass

# Loop through the range of values for i
for i in range(start_i, end_i + 1):
    # Skip if URL is in the error set
    if i in error_urls:
        continue
    url = base_url + str(i) 
    print(i)
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"URL {url} not found (404 error). Adding to error list.")
            error_urls.add(i)
            # Save the error URL to the file
            with open(error_file_path, 'a') as error_file:
                error_file.write(str(i) + '\n')
            continue  # Skip to the next iteration
        else:
            print(f"Error fetching URL {url}: {e}")
            continue  # Skip to the next iteration

    # Parse the HTML content
    total += 1
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find elements with the specified class
    elements = soup.find_all(class_="nutrition nutrition-table infos-block")
    
    for element in elements:
        if len(element.find_all('li')) > 1:
            count += 1

# Print the final count
print(f"Repas avec informations de nutritions: {count} sur un total de {total} repas trouvés")
