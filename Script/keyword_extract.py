import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape issue links and save to a list
def scrape_issue_links():
    print("All links scrape")
    url = "https://www.cambridge.org/core/journals/british-journal-of-political-science/all-issues"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        issue_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            if '/core/journals/british-journal-of-political-science/issue' in href:
                try:
                    year = int(text.split()[2][:4])
                    if year >= 2014:
                        full_link = f"https://www.cambridge.org{href}"
                        issue_links.append(full_link)
                        print(text)
                except (ValueError, IndexError):
                    print("Int value Error ", text)
                    continue

        print(f"Found {len(issue_links)} issue links.")
        return issue_links
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
        return []

# Function to scrape article links from an issue page with pagination
def scrape_article_links(issue_link):
    article_links = []
    current_page = issue_link
    page_number = 1

    while True:
        print(f"Page {page_number}")
        response = requests.get(current_page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/core/journals/british-journal-of-political-science/article' in href:
                    full_link = f"https://www.cambridge.org{href}"
                    article_links.append(full_link)
                    print(f"Found article link: {full_link}")

            # Check for the 'Next Page' button
            next_button = soup.find('a', {'aria-label': 'Next page'})
            if next_button and 'href' in next_button.attrs:
                next_page_url = next_button['href']
                current_page = f"{issue_link}{next_page_url}"
                page_number += 1
                time.sleep(2)  # To avoid overwhelming the server
            else:
                print("No more pages to scrape.")
                break
        else:
            print(f"Failed to retrieve the page: {current_page}. Status code:", response.status_code)
            break

    return article_links

# Function to scrape article details (title, date, keywords)
def scrape_article_details(article_link):
    response = requests.get(article_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title_tag = soup.find('h1', attrs={'data-v-862424e6': True})
        title = title_tag.get_text(strip=True) if title_tag else 'No title found'

        # Extract the published date
        date_tag = soup.find('div', class_='published-date')
        date = date_tag.get_text(strip=True).split('Published online by Cambridge University Press:')[-1].strip() if date_tag else 'No date found'

        # Extract keywords
        keywords_tag = soup.find('div', class_='keywords__pills')
        keywords = ', '.join([span.get_text(strip=True) for span in keywords_tag.find_all('span')]) if keywords_tag else 'No keywords found'

        return title, date, keywords
    else:
        print(f"Failed to retrieve the article page: {article_link}. Status code:", response.status_code)
        return None, None, None

# Function to scrape all articles and save details to an Excel file
def scrape_all_articles():
    issue_links = scrape_issue_links()

    all_articles = []
    temp=0 
    for issue_link in issue_links:
        print(f"Scraping articles from issue - {temp}")
        article_data = scrape_article_links(issue_link)
        all_articles.extend(article_data)
        print(f"Finished scraping articles from issue - {temp}")
        temp+=1

    # Prepare data for DataFrame
    article_details = []
    for article in all_articles:
        title, date, keywords = scrape_article_details(article)
        if title:
            article_details.append({
                'Journal': 'British Journal of Political Science',
                'Date': date,
                'Year': date.split()[-1] if date != 'No date found' else 'Unknown',
                'Title': title,
                'Keywords': keywords,
                'Link': article
            })
        time.sleep(2)  # To avoid overwhelming the server

    # Create a DataFrame
    df = pd.DataFrame(article_details)

    # Save to Excel
    df.to_excel('article_details.xlsx', index=False)
    print("Saved article details to article_details.xlsx")

# Run the functions
scrape_all_articles()
