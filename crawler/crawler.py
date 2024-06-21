import requests
import argparse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_bbox(postal_code, country="Germany"):
    """
    Get the bounding box for a given postal code and country.

    This function uses the Nominatim geocoding service to retrieve the bounding box
    (southwest and northeast coordinates) for the specified postal code.

    Args:
        postal_code (str): The postal code for which to get the bounding box.
        country (str): The country in which the postal code is located. Defaults to "Germany".

    Returns:
        tuple: A tuple containing two tuples, representing the southwest and northeast coordinates of the bounding box.

    Raises:
        ValueError: If the location was not found or the bounding box is missing.
        GeocoderTimedOut: If the geocoding service times out.
        GeocoderServiceError: If there is an error with the geocoding service.
    """
    geolocator = Nominatim(user_agent="pistachiocrawler")

    try:
        location = geolocator.geocode({"postalcode": postal_code, "country": country}, exactly_one=True)
        if location and location.raw.get('boundingbox'):
            bbox = location.raw['boundingbox']
            # The bounding box is provided as [south_lat, north_lat, west_lng, east_lng]
            sw = (float(bbox[0]), float(bbox[2]))
            ne = (float(bbox[1]), float(bbox[3]))
            return (sw, ne)
        else:
            raise ValueError("Location was not found or bounding box is missing")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        raise e

def expand_bbox(bbox, expand_by=0.1):
    """
    Expand the bounding box by a specified amount.

    This function increases the size of the bounding box by the specified amount in all directions.

    Args:
        bbox (tuple): The original bounding box, represented as a tuple of two tuples (southwest and northeast coordinates).
        expand_by (float): The amount by which to expand the bounding box. Defaults to 0.1.

    Returns:
        tuple: A new bounding box with expanded coordinates.
    """
    expanded_bbox_sw = (bbox[0][0] - expand_by, bbox[0][1] - expand_by)
    expanded_bbox_ne = (bbox[1][0] + expand_by, bbox[1][1] + expand_by)

    return (expanded_bbox_sw, expanded_bbox_ne)

def get_api_data(url):
    """
    Fetch data from the given API endpoint using a GET request.

    Args:
        url (str): The API endpoint URL.

    Returns:
        dict: Response data in JSON format if the request is successful, None otherwise.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error occurs.
        requests.exceptions.RequestException: If a request error occurs.
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
    """
    Get store information based on the provided postal code.

    This function retrieves the bounding box for the given postal code, expands it, and
    fetches store information within the bounding box.

    Args:
        plz (str): The postal code to search for stores.

    Returns:
        dict: A dictionary with store IDs as keys and addresses as values.
    """
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
    """
    Get stock levels for stores.

    This function retrieves stock information for the given store addresses.

    Args:
        address_dict (dict): A dictionary with store IDs as keys and addresses as values.

    Returns:
        dict: A dictionary with store addresses as keys and stock levels as values.
    """
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
