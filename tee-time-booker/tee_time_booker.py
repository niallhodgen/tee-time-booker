import requests
from bs4 import BeautifulSoup
from selenium import webdriver



def getPHPSessionID():
    
    url = 'https://brsgolf.com/belvoir'
    
    session.get(url)

    #print('getPHPSessionID() Cookies *****************')
    # print(session.cookies)
    # print('\n')


def getOtherCookies():
    
    url = 'https://members.brsgolf.com/'
    response = session.get(url)

    print('getOtherCookies() Cookies *****************')
    # print(session.cookies)
    # print('\n')

def getCSRFToken():
    
    login_url = 'https://members.brsgolf.com/belvoir/login'
    response = session.get(login_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'login_form[_token]'})['value']

    # print(response.status_code)
    # print(csrf_token)
    # print(session.cookies)

    return csrf_token


def getTimeSheet(csrf_token):

    # Replace 'YOUR_USERNAME'and 'YOUR_PASSWORD'with your actual login credentials
    username = '10773134'
    password = '20Diesel08'

    # Perform the login and obtain the necessary authentication token or cookies
    login_url = 'https://members.brsgolf.com/belvoir/login'

    payload = f'login_form%5Busername%5D={username}&login_form%5Bpassword%5D={password}&login_form%5Blogin%5D=&login_form%5B_token%5D={csrf_token}'
    headers = {
    'Authority': 'members.brsgolf.com:',
    'Method': 'POST',
    'Path': '/belvoir/login',
    'Scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://members.brsgolf.com',
    'Referer': 'https://members.brsgolf.com/belvoir/login'
    }

    response = session.post(login_url, headers=headers, data=payload)

    # Check if the login was successful and retrieve the necessary authentication information
    if response.status_code == 200:
        print('<--- LOGIN SUCCESSFUL! --->')
        # print('TEE TIME REFS......................')
        # print(session.cookies)

    else:
        print('Login failed.')
        print(response.status_code)
        print(response.reason)

# Selenium webdriver is required to access token values and other identifiers that are generated
# via Javascript and hiddden in the HTML page source. Other libraries could not render the Javascript
# properly; hence, it was a last resort.
#
# The key value needed is a href for each booking slot that contains a dynamically generated token
def getDynamicHTML(date):

    url = f'https://members.brsgolf.com/belvoir/tee-sheet/1/{date}'

    # Create a new Chrome browser instance using Selenium
    driver = webdriver.Chrome()

    # Initial page load to pull down and align cookie domains
    driver.get(url)

    # delete the current cookies
    driver.delete_all_cookies()

    # Convert CookieJar to Selenium's dictionary format
    cookies_dict = {}
    
    for cookie in session.cookies:
        # Omit cookie expiry property if the cookie is a session cookie
        if cookie.expires == None:
            cookies_dict[cookie.name] = {
                'name': cookie.name,
                'value': cookie.value,
                'path': cookie.path,
                'domain': cookie.domain,
                'secure': cookie.secure
            }
        else:
            cookies_dict[cookie.name] = {
                'name': cookie.name,
                'value': cookie.value,
                'path': cookie.path,
                'domain': cookie.domain,
                'secure': cookie.secure,
                'expiry': cookie.expires
            }

        driver.add_cookie(cookies_dict[cookie.name])
    
    # Give time for all HTML to load, otherwise it is intermittently missed
    driver.implicitly_wait(3)

    # Navigate to the webpage using Selenium
    driver.get(url)

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    return page_source

def hrefParser(dynamic_html, tee_time_preferences):

    soup = BeautifulSoup(dynamic_html, "html.parser")

    # Find the all timesheet rows
    tr_elements = soup.find_all("tr", class_="bg-white even:bg-grey-faded")

    # Initialise empty array and flag
    available_tee_times_hrefs = []
    tee_time_available = True

    for time in tee_time_preferences:
        # Find <tr> elements containing tee times
        for tr_element in tr_elements:
            tee_time_available = True  # Reset tee_time_available for each tr_element
            if time in tr_element.text:
                # Multiple conditions in above did not work consistently.
                # Div elements separated for filtering
                div_elements = tr_element.find_all("div")
                for div_element in div_elements:
                    # All bookings with 1-4 players have '18 Holes' text added to first column
                    if 'Holes' in div_element.text:
                        tee_time_available = False

                # If 'Holes' isn't in the table row then all 4 slots available
                if tee_time_available:           
                    # Find the anchor tag and extract its href value
                    anchor_tag = tr_element.find('a')
                    if anchor_tag and 'href' in anchor_tag.attrs:
                        href_value = anchor_tag['href']
                        available_tee_times_hrefs.append(href_value)
    
    # print('PAGE SOURCE......................')
    # print(soup)
    print('TEE TIME REFS......................')
    print(available_tee_times_hrefs)

    return available_tee_times_hrefs

def bookingSlotTokens(available_tee_times_hrefs):

    tokens_array = []  # Create an empty dictionary to store the tokens

    for hrefs in available_tee_times_hrefs:

        tokens_array_inner = []
        url = f'https://members.brsgolf.com{hrefs}'
        response = session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        token_1 = soup.find('input', {'name': 'member_booking_form[token]'})['value']     
        token_2 = soup.find('input', {'name': 'member_booking_form[_token]'})['value']
    
        # Add the tokens to the array
        tokens_array_inner.append(token_1)
        tokens_array_inner.append(token_2)
        tokens_array.append(tokens_array_inner)

    print('MEMBER TOKENS......................')
    print(tokens_array)
    
    return tokens_array


def bookTeeTime(hrefs, tokens, player_1, player_2="", player_3="", player_4=""):
    
    i = 0
    status_code = 0

    # Tries to book initial time slot (href), if it fails, it then tries the 2nd, and so on.
    # hrefs array can only be max length of three, so it will only try three times at most.
    while status_code != 200 and i < len(hrefs):
        split_date_time = hrefs[i].split('/')
        time = split_date_time[-1]
        date = split_date_time[-2]

        url = f"https://members.brsgolf.com/belvoir/bookings/store/1/{date}/{time}"

        payload = {
            f'member_booking_form[token]': {tokens[i][0]},
            'member_booking_form[holes]': '18',
            f'member_booking_form[player_1]': {player_1},
            f'member_booking_form[player_2]': {player_2},
            'member_booking_form[guest-rate-2]': '',
            f'member_booking_form[player_3]': {player_3},
            'member_booking_form[guest-rate-3]': '',
            f'member_booking_form[player_4]': {player_4},
            'member_booking_form[guest-rate-4]': '',
            'member_booking_form[vendor-tx-code]': '',
            f'member_booking_form[_token]': {tokens[i][1]}
        }

        # For whatever reason, a successful request requires an empty files array
        files=[]

        response = session.post(url, data=payload, files=files)

        i += 1
        status_code = response.status_code
    
        return response
    

if __name__ == "__main__":

    session = requests.Session()
    tee_time_preferences = ["12:50"]
    tee_time_date = '2023/07/20'

    # player variables
    niall = '3072'
    ed = '3719'
    dave = '3291'

    player_1 = niall
    player_2 = ed
    player_3 = dave

    getPHPSessionID()
    getOtherCookies()
    csrf_token = getCSRFToken()
    getTimeSheet(csrf_token)
    dynamic_html = getDynamicHTML(tee_time_date)
    available_tee_times_hrefs = hrefParser(dynamic_html, tee_time_preferences)
    booking_tokens = bookingSlotTokens(available_tee_times_hrefs)
    response = bookTeeTime(available_tee_times_hrefs, booking_tokens, player_1)