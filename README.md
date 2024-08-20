# journal-keywords-extract


# Journal Keywords Scraper

This Python script scrapes article details from Journals published by Cambridge University Press. It extracts information such as article titles, publication dates, and keywords from all issues, and saves the data in an Excel file.

## Usage
- Clone or download the repository to your local machine.
- Navigate to the script directory in your terminal.
- Run the script using Python:
  ```bash
  python keyword_extract.py

## Features

- **Scrape Issue Links**: Fetches all issue links from a given journal. To scrape from a different journal, update the base URL (`url` variable) in the `scrape_issue_links()` function. The start and end years can be modified as required to target specific publication years.
- **Scrape Article Links**: For each issue, it retrieves all the article links, including those on subsequent pages.
- **Scrape Article Details**: Extracts details like the article's title, publication date, and keywords.
- **Save to Excel**: Compiles the scraped data and saves it to an Excel file (`article_details.xlsx`).

## Requirements

Before running the script, ensure you pip install the following Python libraries installed:

  ```bash
  pip install requests beautifulsoup4 pandas
