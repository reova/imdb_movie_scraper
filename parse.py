from bs4 import BeautifulSoup
from os.path import basename
import requests


COOKIES = {
    'session-id': '143-3087570-5418948',
    'session-id-time': '2082787201l',
    'csm-hit': 'tb:s-40V56D8Z5MGVCJS15RB4|1678002678485&t:1678002678519&adb:adblk_no',
    'ubid-main': '133-9015066-5041153',
    'session-token': 'm0eH5aaF8jB6TMu/LeI+AzNkmyCZqmdDiInuEWQoYFCBsRfEVej/iSxxCEQ05qxImKWuv2h6BOllpw1e1v0FrsvT8+de0332DuHHBugBaBy4vhTq6MEbZka9LWaEoZ5qoZ959J8Apa+W1ec2Ha4Rm+R5gQpJrH7laDV9YVvc87sMZuWHLDihYZ0iAmXN/ro2VAZzW6+NgOTcymX5faAFsw',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Alt-Used': 'www.imdb.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'session-id=143-3087570-5418948; session-id-time=2082787201l; csm-hit=tb:s-40V56D8Z5MGVCJS15RB4|1678002678485&t:1678002678519&adb:adblk_no; ubid-main=133-9015066-5041153; session-token=m0eH5aaF8jB6TMu/LeI+AzNkmyCZqmdDiInuEWQoYFCBsRfEVej/iSxxCEQ05qxImKWuv2h6BOllpw1e1v0FrsvT8+de0332DuHHBugBaBy4vhTq6MEbZka9LWaEoZ5qoZ959J8Apa+W1ec2Ha4Rm+R5gQpJrH7laDV9YVvc87sMZuWHLDihYZ0iAmXN/ro2VAZzW6+NgOTcymX5faAFsw',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

MAIN_URL = 'https://www.imdb.com'

def parse_html(url):  # parse HTML
    response = requests.get(url, cookies=COOKIES, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # title
    title = soup.find(attrs={'data-testid': 'hero-title-block__title'}).text

    # rating 
    rating = soup.find(attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).find('span').text

    # genres
    genres_html = soup.find(attrs={'data-testid': 'genres'}).find_all('a')
    genres_list = []
    
    for genre in genres_html:
        genres_list.append(genre.text)
    
    genres = ' &#x2022; '.join(genres_list)

    # storyline
    storyline = soup.find(attrs={'data-testid': 'plot'}).find(attrs={'data-testid': 'plot-xl'}).text
    
    # director, writers, stars
    div_soup = soup.find(attrs={'data-testid': 'title-pc-wide-screen'}).find_all(attrs={'data-testid': 'title-pc-principal-credit'})
    
    # director
    director = div_soup[0].find('a').text
    
    # writers
    writers_html = div_soup[1].find('ul').find_all('a')
    writers_list = []
    
    for writer in writers_html: 
        writers_list.append(writer.text)
    
    writers = ' &#x2022; '.join(writers_list)

    # stars
    stars_html = div_soup[2].find('ul').find_all('a')
    stars_list = []
    
    for star in stars_html:
        stars_list.append(star.text)

    stars = ' &#x2022; '.join(stars_list)

    # poster
    poster_dir = 'poster/'
    poster_url = soup.find(class_="ipc-lockup-overlay ipc-focusable")['href']
    poster_response = requests.get(
        MAIN_URL + poster_url, cookies=COOKIES, headers=HEADERS)
    poster_soup = BeautifulSoup(poster_response.content, 'html.parser')
    poster = requests.get(poster_soup.find(class_="sc-7c0a9e7c-0 fEIEer")['src']).content

    # images
    images = []
    images_dir = 'images/'
    images_url = soup.find(attrs={'data-testid': 'photos-title'}).find('a')['href']
    images_response = requests.get(
        MAIN_URL + images_url, cookies=COOKIES, headers=HEADERS
    )
    images_soup = BeautifulSoup(images_response.content, 'html.parser')
    get_images_link = images_soup.find(class_='media_index_thumb_list').find_all('a')[:10]

    for image_link in get_images_link:
        image_response = requests.get(
            MAIN_URL + image_link["href"], cookies=COOKIES, headers=HEADERS
        )
        image_soup = BeautifulSoup(image_response.content, 'html.parser')
        image = image_soup.find(attrs={'data-testid': 'media-viewer'}).find('img')['src']
        images.append(requests.get(image).content)
    
    # release date
    release_date = soup.find(attrs={'data-testid': 'title-details-section'}).find(class_='ipc-inline-list__item').find('a').text

    # runtime
    runtime = soup.find(attrs={'data-testid': 'title-techspecs-section'}).find(class_='ipc-metadata-list__item').find('div').text


    return {
        'title': title,
        'poster': poster,
        'rating': rating,
        'genres': genres,
        'director': director,
        'writers': writers,
        'stars': stars,
        'release_date': release_date,
        'runtime': runtime,
        'storyline': storyline,
        'images': images,
        }