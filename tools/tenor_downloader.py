# downloads source gifs from Tenor directly
# this is designed to be imported as a module, not a script
# by: WeegeeNumbuh1
# Valid as of: May 2026

import requests
try:
    from fake_useragent import UserAgent
except ImportError:
    print("This script requires the \'fake_useragent\' module.")
    print("You can install it using \'pip install fake_useragent\'")
    raise
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    print("This script requires the \'BeautifulSoup\' module.")
    print("You can install it using \'pip install beautifulsoup4\'")
    raise
import re
from pathlib import Path

mambo_session = requests.session()
user = UserAgent(browsers=['Chrome', 'Edge', 'Firefox'], platforms='desktop')
HTML_header = {'User-Agent': str(user.random)}
mambo_session.headers = HTML_header

def fetch(url: str, path: str) -> dict:
    """ Parses the HTML, grabs the direct link, then saves the
    gif in `path`. Returns a dict summarizing what was done with the following keys:
    `{'url': str,
    'failure': str|None,
    'gif_url': str|None,
    'gif_keywords': str|None,
    'gif_desc': str|None,
    'gif_upload': str|None,
    'gif_author': str|None,
    'size_MiB': float|None,
    'path': str|None}`.
    """
    result_dict = {
        'url': url,
        'failure': None,
        'gif_url': None,
        'gif_keywords': None,
        'gif_desc': None,
        'gif_upload': None,
        'gif_author': None,
        'size_MiB': None,
        'path': None
    }

    try:
        mambo = mambo_session.get(url, timeout=10)
        mambo.raise_for_status()
    except Exception as e:
        result_dict['failure'] = f'{e}'
        return result_dict

    mambo_soup = bs(mambo.content, 'html.parser')
    # navigate to the img tag inside the div with class "Gif"
    # The structure is:
    # div.GifPage -> div.main-container -> div.single-view-container -> div ->
    # div#single-gif-container -> div[itemprop="image"] ->
    # if sticker: div.Sticker -> img
    # elif meme: div.Meme -> img
    # else: div.Gif -> img

    gif_div = mambo_soup.find(id="single-gif-container")
    if gif_div:
        # the below does not link to the direct gif (don't use, but left here anyway)
        # contentURL = gif_div.find('meta', attrs={'itemprop': 'contentUrl'})

        img_tag = gif_div.find('img')
        if img_tag:
            src_value = img_tag.get('src')
            if not src_value:
                result_dict['failure'] = "Failed to find main GIF on the webpage."
                return result_dict
            result_dict['gif_url'] = src_value
            if (uploaddate := gif_div.find('meta', attrs={'itemprop': 'uploadDate'})):
                result_dict['gif_upload'] = uploaddate.get('content')
            if (gifauthor := gif_div.find('meta', attrs={'itemprop': 'author'})):
                result_dict['gif_author'] = gifauthor.get('content')
            if (keywords := gif_div.find('meta', attrs={'itemprop': 'keywords'})):
                result_dict['gif_keywords'] = keywords.get('content')
            result_dict['gif_desc'] = img_tag.get('alt')
    else:
        result_dict['failure'] = "Failed to find main GIF on the webpage."
        return result_dict

    canonical_link = mambo_soup.find('link', rel='canonical')
    if canonical_link:
        href = canonical_link.get('href', '')
        match = re.search(r'/view/([^/?#]+)', href)
        if match:
            view_id = match.group(1)
        else:
            result_dict['failure'] = f'Could not determine canonical link in link: {href}'
            return result_dict
    else:
        result_dict['failure'] = "No canonical link found"
        return result_dict
    save_path = Path(path, f'{view_id}.gif')
    result_dict['path'] = f'{save_path}'
    if save_path.exists():
        result_dict['failure'] = "File already exists, not downloading gif."
        return result_dict
    try:
        mambo_gif = mambo_session.get(str(result_dict['gif_url']), timeout=10)
        mambo_girth = len(mambo_gif.content)
        mambo_gif.raise_for_status()
    except Exception as e:
        result_dict['failure'] = f"Failed to download gif: {e}"
        return result_dict
    result_dict['size_MiB'] = round(mambo_girth / 1024 ** 2, 3)
    with open(Path(path, f'{view_id}.gif'), 'wb') as f:
        f.write(mambo_gif.content)
    return result_dict