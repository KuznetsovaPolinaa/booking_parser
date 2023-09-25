# Web Scraper of Booking.com 🏢

Scraper extracts data from the hotel page on Booking.com and save it in a file.

We get the following hotel's information:
- Name
- Address
- Rating
- Popular facilities
- Pet policy
- Payment methods
- Room types and their lowest price

## How to use 💻

1. Create a virtual environment
2. Install requirements `pip install -r requirements.txt`
3. Run `python main.py`
4. Copy and paste hotel page's URL into terminal
5. Open a new file: [example.json](example.json)

## Notes 📝

* There may be some inconsistencies with the selected currency since Booking.com automatically 
  chooses currency based on web scrapers' IP address' geographical location. There are two 
  ways to fix this: use a proxy of a specific location or manually change the currency in the URL. If there is no currency parameter
  in the URL, just add it manually to the end of the URL, after the and sign(&) or the semicolon(;) and 
  before the hashtag(#) as in the example below:

  https://www.booking.com/hotel ... &**selected_currency=USD**# ...


* Also, if the URL does not have checkin and chechout parameters, it is recommended to add it to the URL as well for 
  more accurate data extraction. Since the information of room types and their prices may be missing. Here is the example:

  https://www.booking.com/hotel ... &**checkin=2023-12-30**&**checkout=2023-12-31**& ...
