import requests
import argparse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_bbox(postal_code, country="Germany"):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.geocode({"postalcode": postal_code, "country": country}, exactly_one=True)
        if location and location.raw.get('boundingbox'):
            bbox = location.raw['boundingbox']
            # The bounding box is provided as [south_lat, north_lat, west_lng, east_lng]
            sw = (float(bbox[0]), float(bbox[2]))
            ne = (float(bbox[1]), float(bbox[3]))
            return (sw, ne)
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error: {e}")
        return None, None

def expand_bbox(bbox, expand_by=0.1):
    expanded_bbox_sw = (bbox[0][0] - expand_by, bbox[0][1] - expand_by)
    expanded_bbox_ne = (bbox[1][0] + expand_by, bbox[1][1] + expand_by)

    return (expanded_bbox_sw, expanded_bbox_ne)


def get_api_data(url):
    """
    Fetch data from the given API endpoint using GET request.

    :param url: The API endpoint URL.
    :param params: (Optional) Dictionary of query parameters to append to the URL.
    :return: Response data in JSON format if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the response contains JSON data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    return None

def get_stores(plz):
    bbox = get_bbox(plz)
    ebbox = expand_bbox(bbox)

    store_url = f"https://store-data-service.services.dmtech.com/stores/bbox/{ebbox[1][0]}%2C{ebbox[0][1]}%2C{ebbox[0][0]}%2C{ebbox[1][1]}?countryCode=DE&fields=storeId,address"

    store_data = get_api_data(store_url)

    ids = [store_data['stores'][i]['storeId'] for i in range(len(store_data['stores']))]
    addresses = [store_data['stores'][i]['address']['street'] + ", " + store_data['stores'][i]['address']['zip']
                 for i in range(len(store_data['stores']))]

    address_dict = dict(zip(ids, addresses))
    return address_dict

def get_stocks(address_dict):
    ids = list(address_dict.keys())
    stock_url = "https://products.dm.de/store-availability/DE/availabilities/map/dans/1304593?storeIds=" + ",".join(ids)
    stock_data = get_api_data(stock_url)

    stock_dict = {}

    for k, d in stock_data['storeAvailabilitiesByStoreId'].items():
        if d['status']['code'] == 'OK':
            stock_dict[address_dict[k]] = d['stockLevel']

    return stock_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get stocks from stores.')
    parser.add_argument('plz', type=int, help='Zip code to get stores')

    args = parser.parse_args()

    stores = get_stores(args.plz)
    stocks = get_stocks(stores)
    print(stocks)
