from django.shortcuts import render

def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content 

def home(request):
    weather = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather = dict()
        # extract region
        weather['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        # extract temperature now
        weather['time'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        # get the day, hour and actual weather
        weather['status'], weather['temp'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
            
    return render(request, 'home.html', {'weather': weather})