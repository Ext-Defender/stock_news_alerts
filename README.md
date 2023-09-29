# Stock News SMS alert Script
## Description
This simple script checks if the percent change of the openning and closing prices of a specified stock. If the change is at or greater than 5%, then sends a sms alert via Twilio to your phone with how much the price jump was and three relevant news article headlines to provide a brief of what is being said about the company in question.

## Getting started (WIP)
- pip install -r requirements.txt
- define environment variables
- python .\main.py

### Environment Variables
- STOCK_API_KEY - https://www.alphavantage.co
- NEWS_API_KEY - https://newsapi.org/v2/everything
- TWILIO_SID
- TWILIO_API_KEY
- TWILIO_NUMBER
- MY_NUMBER
