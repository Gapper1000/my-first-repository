from getpass import getpass

import os
import json
from pprint import pprint
from statistics import mean

from dotenv import load_dotenv
import requests
from plotly.express import line

from app.email_service import send_email


load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print(API_KEY)

#breakpoint()

#quit()



request_url = f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={API_KEY}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)
print(type(parsed_response))
print(parsed_response.keys())
#pprint(parsed_response)

data = parsed_response["data"]

# Challenge A
#
# What is the most recent unemployment rate? And the corresponding date?
# Display the unemployment rate using a percent sign.

print("-------------------------")
print("LATEST UNEMPLOYMENT RATE:")
#print(data[0])
print(f"{data[0]['value']}%", "as of", data[0]["date"])


# Challenge B
#
# What is the average unemployment rate for all months during this calendar year?
# ... How many months does this cover?


this_year = [d for d in data if "2023-" in d["date"]]

rates_this_year = [float(d["value"]) for d in this_year]
#print(rates_this_year)

print("-------------------------")
print("AVG UNEMPLOYMENT THIS YEAR:", f"{round(mean(rates_this_year), 2)}%")
print("NO MONTHS:", len(this_year))

# Challenge C
#
# Plot a line chart of unemployment rates over time.


dates = [d["date"] for d in data]
rates = [float(d["value"]) for d in data]

fig = line(x=dates, y=rates, title="United States Unemployment Rate over time", labels= {"x": "Month", "y": "Unemployment Rate"})
fig.show()


user_address = input("Please enter your email address: ")



latest_rate = data[0]['value']
latest_date = data[0]["date"]

content = f"""
<h1> Unemployment Report Email </h1>

<p> Latest rate: {latest_rate}% as of {latest_date} </p>
"""

send_email(recipient_address=user_address, html_content=content, subject="Your Unemployment Report")