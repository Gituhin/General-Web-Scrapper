# General-Web-Scrapper
## Scrapes professors' details from various institutes integrated with Google Sheets

This web scrapper uses Beautiful Soup python package to extract HTML content from a webpage. Then it finds desired HTML tags and their texts from the extracted content.

Since web scrapping is very a webpage specific process, but still I tried hard to keep it very general for all possible institute websites. I used Google sheets as a frontend dashboard for inputting various values and parameters. And the scrapped data is directly appended in the sheet itself reducing need to upload or copy/paste data. The actual web scrapper is run by a HTTP trigger hosted at wayscript but anyone can manually run it on any supported python IDE manually.
