import requests

import spotify.sync as spotify

base_url = "https://api.spotify.com"

response = requests.get(f"{base_url}")

response_json = response.json()
print(response_json)

#   curl -X POST "https://accounts.spotify.com/api/token" \
#        -H "Content-Type: application/x-www-form-urlencoded" \
#        -d "grant_type=client_credentials&client_id=8031aca9a95441ec9f7d4184008ebe96&client_secret=7cc11d4eb2e34c4f9c8a562a0ca1ec59"


#   curl "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb" \
#        -H "Authorization: Bearer BQCczFtBb5krXpXEtkDXhWkkAMAa1Ho1ZWq0vinbTxFrgzRzTn1tg1Q7WgGwZKuBIR4BsTAZIhb40l8b8PWRrYZo4NRbzTDalZQTR-IQFpULpiNMLPI"
