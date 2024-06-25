from bs4 import BeautifulSoup
import requests
import os
import datetime
import glob
# Define the output folder path
output_folder = r"F:\DonotDelete\Nahid.Hasan\Desktop\Whatsapp_Update"

# URL of the API endpoint
url = "https://store.rg-adguard.net/api/GetFiles"

# Construct the payload as a dictionary
payload = {
    "type": "url",
    "url": "https://www.microsoft.com/store/productId/9NKSQGP7F2NH",
    "ring": "RP",
    "lang": "en-US"
}

# Text to check for in the HTML response
text_to_check = "WhatsAppDesktop_"

try:
    # Sending POST request with payload
    response = requests.post(url, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful!")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all occurrences of the text in the HTML
        results = soup.find_all(string=lambda text: text and text_to_check in text)

        # Initialize lists to store links and filenames
        links = []
        filenames = []

        # Iterate over each result and extract link and filename
        for result in results:
            # Get the parent element of the text
            parent_element = result.find_parent()

            # Extract the link from the 'href' attribute of the parent <a> tag
            link = parent_element.get('href')

            # Extract the filename from the text inside the <a> tag
            filename = result.strip()  # assuming result is the filename text

            # Append to lists
            links.append(link)
            filenames.append(filename)

        # Print the extracted links and filenames
        print("Links:")
        print(links)
        print("Filenames:")
        print(filenames)

    else:
        print(f"Request failed with status code {response.status_code}")

except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    
# Ensure the directory where you want to save the file exists
#download_dir = r'F:\DonotDelete\Nahid.Hasan\Desktop\Whatsapp_Update'  # Replace with your desired directory path
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Index 1 corresponds to the second link and filename in your lists
url_to_download = links[1]
filename_to_save = filenames[1]

# Ensure the filename is valid and doesn't contain illegal characters for filenames
#valid_filename = filename_to_save.replace('/', '_')  # Replace '/' with '_' for safe filename

# Combine the directory path and filename to get the full path where the file will be saved
full_path = os.path.join(output_folder, filename_to_save)

try:
    # Check if the file already exists
    if os.path.exists(full_path):
        now = datetime.datetime.now()
        exist=f"\nFile '{filename_to_save}' already exists. Skipping download.\nExecuted in {now}"
        output_file = output_folder + r"\output.txt"
        with open(output_file, 'a') as f:
            f.write(exist)

    else:
        existing_files = glob.glob(os.path.join(output_folder, '*.msixbundle'))
        for file_path in existing_files:
            os.remove(file_path)
        print(f"Deleted: {file_path}")
        # Send a GET request to download the file
        response = requests.get(url_to_download)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"Downloading {url_to_download} as {full_path}")
            # Write the content to the file
            with open(full_path, 'wb') as f:
                f.write(response.content)
            now = datetime.datetime.now()
            downloaded=f"\nFile Downloaded Successfully.\nExecuted in {now}"
            output_file = output_folder + r"\output.txt"
            with open(output_file, 'a') as f:
                f.write(downloaded)

        else:
            now = datetime.datetime.now()
            failed=f"Failed to download file, status code: {response.status_code}.\nExecuted in {now}"
            output_file = output_folder + r"\output.txt"
            with open(output_file, 'a') as f:
                f.write(failed)
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")    
    now = datetime.datetime.now()
    reqer=f"Failed to download file, status code: {response.status_code}.\nExecuted in {now}"
    output_file = output_folder + r"\output.txt"
    with open(output_file, 'a') as f:
                f.write(reqer)
