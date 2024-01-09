import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from . import *

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("GET from {} ".format(url))

    try:
        # Call get method of requests library with URL and parameters
        if "analyzeparams" in kwargs:
            params = kwargs['analyzeparams']
            return requests.get(url, params=params, headers={'Content-Type': 'application/json'},auth=HTTPBasicAuth('apikey', params['api_key']))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},params=kwargs)
            json_data = json.loads(response.text)
            return json_data 
    except:
        # If any error occurs
        print("Network exception occurred")



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)
        response.raise_for_status()
        json_data = json.loads(response.text)
        return json_data
    
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)

    

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print("JSON Result:", json_result)  # Add this line to inspect the JSON structure

    if json_result and "body" in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results



# get_dealer_by_id_from_cf
def get_dealer_by_id_from_cf(url, _dealerId):
    result = []
# - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=_dealerId)
    if json:
# - Parse JSON results into a DealerView object list
        dealer = json_result["rows"]
        dealer_doc = dealer["doc"]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
        result.append(dealer_obj)
    return result


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    
    if json_result:
        reviews = json_result['rows']
        for review_ in reviews:
            review = review_["doc"]
            results.append(DealerReview(
                name = review["name"],
                dealership = review["dealership"], 
                review = review["review"], 
                createdAt = review["createdAt"],  
                purchase=review["purchase"],                    
                sentiment = analyze_review_sentiments(review['review']),
                purchase_date = review["purchase_date"] if "purchase_date" in review else False, 
                car_make = review['car_make'] if 'car_make' in review else False,
                car_name = review['car_model'] if 'car_model' in review else False,
                car_type = "no data", 
                car_year= review['car_year'] if 'car_year' in review else False, 
                id=review["_id"]
                ))
            
              
            """  results.append(DealerReview(name = review["name"], createdAt = review["createdAt"],
            dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
            purchase_date = 'none', car_make = 'none', car_name='none',
            sentiment = analyze_review_sentiments(review['review']),
            car_type = 'none', car_year= 'none', id=review["_id"])) """
                
    return results


def save_review(url, review):
    result = post_request(url, review)
    print(result)
    return result   




# ---------------------------------------------------------

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):

    url = ANALYZE_PARAMS.get("url")

    params = dict()
    params['text'] = text
    params['api_key'] = ANALYZE_PARAMS.get("api_key")
    params['return_analyzed_text'] = 'true'
    params["version"] = '2020-08-01'
    params["features"] = {
    "sentiment": {}
  }

    print('params: {}'.format(params))

    response = get_request(url, analyzeparams=params)
    status_code = response.status_code
    
    if status_code != 200:
        return {'text': 'noanalyze'}
    else:   
        json_data = json.loads(response.text)
        label = json_data['sentiment']['document']['label'] 
        return {'text': label}