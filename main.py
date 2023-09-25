import requests
from bs4 import BeautifulSoup
import json
import lxml
import string


# Check, if the url is valid
def check_url(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url=url, headers=headers)
    except requests.exceptions.MissingSchema:
        print("Invalid URL")
    else:
        if response.status_code == 200:
            if "selected_currency=" not in url:
                print("There may be some inconsistencies with the currency, check the README file")
            if ("checkin_monthday=" and "checkin=") not in url:
                print("There may be no data about rooms' types and their prices, check the README file")
            return response
        else:
            print("Problem with the request")


# Get the data about a hotel
def get_data(url):
    if (response := check_url(url)):
        print("Collecting information, please, wait...")

        soup = BeautifulSoup(response.text, "lxml")

        # The dictionary with all information about the hotel
        hotel = {}

        # Get a name of the hotel
        hotel["name"] = soup.find("h2", {"class":"pp-header__title"}).text.strip()

        # Get an address of the hotel
        hotel["address"] = soup.find("span", {"class":"hp_address_subtitle"}).text.strip()

        # Get a rating of the hotel
        hotel["rating"] = soup.find("div", {"class":"a3b8729ab1 d86cee9b25"}).text

        # Get a list of the most popular facilities of the hotel
        facilities = soup.find_all("div", {"class":"ab06168e66"})
        list_of_fac = []
        for i in facilities[:(len(facilities))//2]:
            list_of_fac.append(i.text.strip())

        hotel["popular_facilities"] = list_of_fac

        # Get the hotel pet policy
        hotel["pet_policy"] = soup.find("div", {"class":"description description--house-rule"}).find_all("p")[1].text.strip()

        # Get a list of payment methods
        payments = soup.find("p", {"class":"payment_methods_overall"}).find_all("img")
        list_of_p = []
        for i in payments:
            list_of_p.append(i["title"])
        
        try:
            cash = soup.find("span", {"class":"bui-badge__text"}).text.strip()
        except:
            cash = None

        if cash is not None:
            list_of_p.append(cash)

        hotel["payment_methods"] = list_of_p

        # Get the information about room types and their prices
        # A list of all room rates' ids
        ids = []

        try:
            trs = soup.find_all("tr")
        except:
            trs = None

        for i in trs:
            try:
                id = i.get('data-block-id')
            except:
                id = None
            if id is not None:
                ids.append(id)

        # A list of room types and prices
        rooms_and_prices = []

        for i in ids:
            # The dictionary with room type and its lowest price
            rate = {}

            try:
                id_data = soup.find("tr", {"data-block-id":i})
                
                try:
                    room = id_data.find("span", {"class":"hprt-roomtype-icon-link"})
                except:
                    room = None

                if room is not None:
                    rate["room_type"] = room.text.strip()
                    price = id_data.find("div",{"class":"bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading"})
                    rate["price"] = price.text.strip().replace("\xa0", "")

                if rate:
                    rooms_and_prices.append(rate)
            
            except:
                rate["room_type"] = None
                rate["price"] = None
                
        # Add room types and prices to the main dictionary
        hotel["rooms_and_prices"] = rooms_and_prices

        return hotel


# Save as a json file
def save_data(url):
        hotel = get_data(url)
        hotel_name = hotel['name']

        file_name = ""

        # The name of the file will be the name of the hotel
        for i in hotel_name:
            if i in (string.ascii_letters+string.digits):
                file_name += i
            elif i == " " and file_name[-1] != "_":
                file_name += "_"

        with open(f"{file_name}.json", "w", encoding="utf-8") as file:
            json.dump(hotel, file, indent=4, ensure_ascii=False)



def main():
    url = input("Enter the URL of hotel: ")
    save_data(url)



if __name__ == "__main__":
    main()