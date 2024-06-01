import pandas as pd
import imdb
import asyncio

# Initialize IMDbPY
ib = imdb.IMDb()

# Function to fetch poster URL asynchronously
async def get_poster_url_async(title):
    try:
        search_title = ib.search_movie(title)
        movie = search_title[0]
        ib.update(movie)
        poster_url = movie.get("full-size cover url")

        return poster_url
    except Exception as e:
        print(f"Error fetching poster URL for '{title}': {e}")
        return None
    
# Read the CSV file
df = pd.read_csv("netflix_titles.csv")

# Asynchronous function to fetch poster URLs for all titles
async def fetch_poster_urls():
    tasks = []
    for title in df['title']:
        tasks.append(get_poster_url_async(title))
    return await asyncio.gather(*tasks)

# Run the event loop
loop = asyncio.get_event_loop()
poster_urls = loop.run_until_complete(fetch_poster_urls())

# Update the DataFrame with poster URLs
df['poster_url'] = poster_urls

# Save the updated DataFrame to CSV
df.to_csv("Updated_netlix_titles.csv", index=False)
