import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Send request to Google News
url = "https://news.google.com/topstories"
response = requests.get(url)

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all news article elements
articles = soup.find_all('article')

# Create a list to store news article data
news_data = []

# Loop through each article element
for article in articles:
    # Extract article title
    title_tag = article.find('h3')
    title = title_tag.text.strip() if title_tag else ""

    # Extract article link
    link_tag = article.find('a')
    link = link_tag['href'] if link_tag else ""

    # Extract article description (as text)
    description_tag = article.find('span', class_='IsZvec')
    description = description_tag.text.strip() if description_tag else ""

    # Combine title and description into 'text' for the dataset
    text = f"{title} {description}".strip()

    # Set label to "REAL" by default
    label = "REAL"

    # Append article data to the list
    news_data.append({
        "title": title,
        "text": text,
        "label": label
    })

# Create a Pandas dataframe
df = pd.DataFrame(news_data)

# Check if the file exists
file_path = "news_data.csv"
if os.path.exists(file_path):
    # Load existing dataset
    existing_df = pd.read_csv(file_path)
    # Append new data to existing dataset
    updated_df = pd.concat([existing_df, df], ignore_index=True)
else:
    # Create a new dataframe
    updated_df = df

# Save updated dataset to CSV file in the required format
updated_df.to_csv(file_path, index=False, columns=["title", "text", "label"])
