import datetime as dt # Import the datetime module (aliased as dt) to work with dates
import random # Import random module to randomly select a letter template
import smtplib # Import smtplib to send emails using SMTP protocol
import pandas # Import pandas to read and work with CSV data
import os

# Placeholder text in the letter templates that will be replaced with a real name
TEXT_TO_REPLACE = "[NAME]"

# The sender's email address
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# Get the current date and time
now = dt.datetime.now()

# Create a tuple containing today's month and day (e.g., (3, 4))
date_today = (now.month, now.day)

# Read the birthdays.csv file into a pandas DataFrame
data = pandas.read_csv("birthdays.csv")

# Create a dictionary:
# Key = (month, day)
# Value = entire row of data for that birthday
all_birthdays = {(row['month'], row['day']): row for (index, row) in data.iterrows()}

# Check if today's date matches any birthday in the dictionary
if date_today in all_birthdays:

    # Randomly choose a number between 1 and 3 to select a letter template
    letter_number = random.randint(1, 3)

    # Open the randomly selected letter template file in read mode
    with open(f"letter_templates/letter_{letter_number}.txt") as letter:

        # Read the entire contents of the template file
        letter_template = letter.read()

    # Replace the placeholder text "[NAME]" with the actual person's name
    email_body = letter_template.replace(
        TEXT_TO_REPLACE,
        all_birthdays[date_today]['name']
    )

    # Create an SMTP connection to Gmail's mail server
    with smtplib.SMTP("smtp.gmail.com") as connection:

        # Secure the connection using TLS encryption
        connection.starttls()

        # Log into the email account using the provided credentials
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)

        # Send the email
        connection.sendmail(
            from_addr=MY_EMAIL,                  # Sender email address
            to_addrs=all_birthdays[date_today]['email'],     # Recipient email address
            msg=f"Subject:Happy Birthday\n\n{email_body}"  # Email subject and body
        )
