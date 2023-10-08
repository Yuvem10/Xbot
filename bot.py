import random
from requests_oauthlib import OAuth1Session
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

consumer_key = '<your_consumer_key>'
consumer_secret = '<your_consumer_secret>'
Username = "username"
Password = "password"

listOfTweet = ["", "", ""]
key = random.choice(listOfTweet)
payload = {"text": key}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)

# driver initialisation
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get(authorization_url)

# login on the verification page
username = driver.find_elements(by='id', value="username_or_email")
password = driver.find_elements(by='id', value="password")
username[0].send_keys(Username)
password[0].send_keys(Password)
button = driver.find_elements(by='id', value="allow")
button[0].click()

# recipe code on the other page
code = driver.find_element(By.CSS_SELECTOR, 'code')
verifier = code.text


# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))
