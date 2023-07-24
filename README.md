# tee-time-booker
An experimental program to automate tee time booking at my local golf club using BRS Golf's API.

Booking tee times has become notoriously difficult since COVID. Tee times are released at 7.30pm, 7 days in advance and they fill up within 5 min of opening, especially for important competitions. The aim of this program is to automate that process and trigger API calls to book times as soon as booking opens.

## Secrets

Both tfvars and .env file with secrets have been excluded from source control via .gitignore. If cloning this repo, please use appropriate secrets management as I have.

## IaC

Terraform has been employed to create an AWS Lambda function that will run at designated times.

## tee_time_booker.py

This script is supplied the following key variables:

### URLs

*club_brs_url = 'https://brsgolf.com/belvoir'
*club_members_brs_url = 'https://members.brsgolf.com/'
*club_login_brs_url = 'https://members.brsgolf.com/belvoir/login'

### Prefs
*tee_time_preferences = ["12:50", "13:00", "20:00"]
*tee_time_date = '2023/07/24'

# Player variables
niall = '3072'
ed = '3719'
dave = '3291'