# from googlesearch import search  # Ensure googlesearch-python is installed

# # Define the search query
# query = "site:kidsandus.es inurl:/es/academias-ingles/"

# # Initialize a set to store unique URLs
# urls = set()

# # Perform the search and iterate over the results
# try:
#     for result in search(query, num_results=500):  # Adjust the number as needed
#         # Split the URL to extract the desired portion
#         parts = result.split("/")
#         if len(parts) > 5:  # Check if there's an additional path after the last segment
#             cleaned_url = "/".join(parts[:6])  # Keep only up to "/academias-ingles/{location}"
#         else:
#             cleaned_url = result.rstrip("/")  # Remove trailing slash if no extra path exists
#         urls.add(cleaned_url)

#     # Save the unique URLs to a file
#     with open("kidsandus_academias_cleaned_urls.txt", "w") as file:
#         for url in sorted(urls):
#             file.write(url + "\n")

#     print(f"Extracted {len(urls)} unique URLs.")
# except Exception as e:
#     print(f"An error occurred: {e}")



# file_path = "kidsandus_academias_urls.txt"  # Replace with your file name

# # Initialize a set to store unique cleaned URLs
# cleaned_urls = set()

# try:
#     # Read the input file line by line
#     with open(file_path, "r") as file:
#         for line in file:
#             url = line.strip()  # Remove any extra whitespace or newline characters
#             if url:
#                 # Split the URL by '/' and extract up to the relevant part
#                 parts = url.split("/")
#                 if len(parts) > 5:  # Check if there are additional paths
#                     cleaned_url = "/".join(parts[:6])  # Keep up to "/academias-ingles/{location}"
#                 else:
#                     cleaned_url = url.rstrip("/")  # Remove trailing slash if no extra path
#                 cleaned_urls.add(cleaned_url)

#     # Remove duplicates by overwriting the original file without bad URLs
#     with open(file_path, "r+") as file:
#         lines = file.readlines()
#         file.seek(0)
#         unique_lines = set()  # To track written lines
#         for line in lines:
#             cleaned_line = line.strip()
#             if cleaned_line in cleaned_urls and cleaned_line not in unique_lines:
#                 file.write(cleaned_line + "\n")
#                 unique_lines.add(cleaned_line)
#         file.truncate()

#     # Append cleaned URLs at the end (if any are missing)
#     with open(file_path, "a") as file:
#         for url in sorted(cleaned_urls - unique_lines):
#             file.write(url + "\n")

#     print(f"Cleaned and appended {len(cleaned_urls)} unique URLs in {file_path}.")
# except Exception as e:
#     print(f"An error occurred: {e}")



# import asyncio
# from playwright.async_api import async_playwright
# import re

# # Function to extract emails
# async def extract_emails():
#     input_file = "links.txt"  # Input file with URLs
#     output_file = "kidsandus_all_emails.txt"  # Output file to save emails

#     # Read URLs from the input file
#     with open(input_file, "r") as file:
#         urls = [url.strip() for url in file.readlines()]
#     with open(output_file, "r") as file:
#         urlsgot = file.read()

#     # Start Playwright
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)  # Set headless=False to see the browser
#         context = await browser.new_context()
#         page = await context.new_page()

#         # Open the output file to save results
#         with open(output_file, "w") as output:
#             for url in urls:
#                 if url in urlsgot:
#                     print(f'pass {url}')
#                     continue
#                 try:
#                     # Navigate to the main URL
#                     await page.goto(url, timeout=60000)

#                     # Wait for the page to load
#                     await page.wait_for_timeout(3000)

#                     # Dismiss the cookie banner if present
#                     try:
#                         cookie_button = page.locator("#onetrust-accept-btn-handler")  # Selector for "Accept" button
#                         if await cookie_button.count() > 0:
#                             await cookie_button.click()
#                             await page.wait_for_timeout(1000)  # Allow time for the banner to disappear
#                     except Exception as e:
#                         print(f"No cookie banner found or issue dismissing: {e}")

#                     # Find the "Contáctanos" button
#                     contact_button = page.locator("text=Contacta'ns")  # Locate the button
#                     if await contact_button.count() > 0:  # Ensure the button exists
#                         await contact_button.first.click()  # Click the first matching button

#                         # Wait for the contact page to load
#                         await page.wait_for_timeout(3000)

#                         # Extract all email addresses from the page content
#                         page_content = await page.content()
#                         emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_content)
#                         emails = [e for e in emails if "kidsandus" in e]  # Filter for Kids&Us-specific emails

#                         # Save all emails found, associating them with the URL
#                         if emails:
#                             output.write(f"{url}: {', '.join(emails)}\n")
#                             print(f"Extracted emails from {url}: {', '.join(emails)}")
#                         else:
#                             print(f"No emails found for {url}")
#                     else:
#                         print(f"No 'Contáctanos' button found on {url}")

#                 except Exception as e:
#                     print(f"Error on {url}: {e}")

#         # Close the browser
#         await browser.close()

# # Run the function
# asyncio.run(extract_emails())






import re

# Input data
raw_data = """
https://www.kidsandus.es/ca/academies-dangles/amposta: amposta@kidsandus.cat, amposta@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/berga: berga@kidsandus.cat, berga@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/hospitalet-centre: hospitalet.centre@kidsandus.es, hospitalet.centre@kidsandus.es, hospitalet.centre@kidsandus.es, hospitalet.centre@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/la-garriga: lagarriga@kidsandus.cat, lagarriga@kidsandus.cat, lagarriga@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/lleida: lleida.barrisnord@kidsandus.cat, lleida.barrisnord@kidsandus.cat, lleida.zonaalta@kidsandus.cat, lleida.zonaalta@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/lleida: lleida.barrisnord@kidsandus.cat, lleida.barrisnord@kidsandus.cat, lleida.zonaalta@kidsandus.cat, lleida.zonaalta@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/lleida: lleida.barrisnord@kidsandus.cat, lleida.barrisnord@kidsandus.cat, lleida.zonaalta@kidsandus.cat, lleida.zonaalta@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/mollerussa: mollerussa@kidsandus.cat, mollerussa@kidsandus.cat, mollerussa@kidsandus.cat, mollerussa@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/noubarris: noubarris@kidsandus.es, noubarris@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/palafrugell: palafrugell@kidsandus.es, palafrugell@kidsandus.es
https://www.kidsandus.es/ca/academias-ingles/palma-nord: palma.nord@kidsandus.es, palma.nord@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/pinedademar: pinedademar@kidsandus.cat, pinedademar@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/andorra: andorralavella@kidsandus.ad, andorralavella@kidsandus.ad
https://www.kidsandus.es/ca/academies-dangles/santandreu: santandreu@kidsandus.cat, santandreu@kidsandus.cat, santandreu@kidsandus.cat, santandreu@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/santfeliudeguixols: sf.guixols@kidsandus.es, sf.guixols@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/santmarti: santmarti@kidsandus.es, santmarti@kidsandus.es, santmarti@kidsandus.es, santmarti@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/sant-quirze: santquirze@kidsandus.cat, santquirze@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/santa-coloma: santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/tordera: tordera@kidsandus.es, tordera@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/vilassar: vilassar@kidsandus.cat, vilassar@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/mollerussa: mollerussa@kidsandus.cat, mollerussa@kidsandus.cat, mollerussa@kidsandus.cat, mollerussa@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/santandreu: santandreu@kidsandus.cat, santandreu@kidsandus.cat, santandreu@kidsandus.cat, santandreu@kidsandus.cat
https://www.kidsandus.es/ca/academies-dangles/santfeliudeguixols: sf.guixols@kidsandus.es, sf.guixols@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/santmarti: santmarti@kidsandus.es, santmarti@kidsandus.es, santmarti@kidsandus.es, santmarti@kidsandus.es
https://www.kidsandus.es/ca/academies-dangles/santa-coloma: santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es, santa.coloma@kidsandus.es

"""

# Parse the raw data to extract all email addresses
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", raw_data)

# Remove duplicate emails
unique_emails = sorted(set(emails))

# Save to a file or print the clean list
output_file = "cleaned_email.txt"
with open(output_file, "w") as file:
    for email in unique_emails:
        file.write(email + "\n")

print(f"Cleaned and deduplicated emails saved to {output_file}.")


