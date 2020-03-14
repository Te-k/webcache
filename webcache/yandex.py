import urllib
import requests
from bs4 import BeautifulSoup


class Yandex:
    @staticmethod
    def search(req):
        '''
        Search for a request in Yandex and return results
        Does not work all the time, Yandex has a captcha often
        '''
        r = requests.get('https://yandex.ru/search/?text=%s' %
                urllib.parse.quote(req, safe='')
        )
        if r.status_code != 200:
            return False, []

        soup = BeautifulSoup(r.text, 'lxml')
        if soup.find('main') is None:
            return False, []
        res = []
        for l in soup.find_all('li', class_='serp-item'):
            url = l.a['href']
            result = {
                'url': l.a['href'],
                'name': l.a.text,
            }
            text = l.find('div', class_="text-container")
            if text:
                result['text'] = text.text
            popup = l.find_all('div', class_='popup2')
            if len(popup) > 0:
                for link in popup[0].find_all('a'):
                    if 'translate.yandex.ru' in link['href']:
                        if link['href'].startswith('http'):
                            result['translate'] = link['href']
                        else:
                            result['translate'] = 'http:' + link['href']
                    if 'yandexwebcache.net' in link['href']:
                        result['cache'] = link['href']
            res.append(result)

        return True, res

    @staticmethod
    def download_cache(cache_url):
        '''
        Extract content from a cached Yandex url
        '''
        # FIXME: do not get date and url
        r = requests.get(cache_url)
        if r.status_code == 200:
            return {
                'success': True,
                'data': r.text[:-90],
                'cacheurl': cache_url,
            }
        else:
            return {'success': False}

    @staticmethod
    def cache(url):
        """
        Search for a cache url in yandex and if found get its content
        """
        # FIXME: miss obvious pages, like www.domain.com instead of domain.com
        v, res = Yandex.search(url)
        if v:
            for i in res:
                if i['url'] == url:
                    if 'cache' in i:
                        c = Yandex.download_cache(i['cache'])
                        c['found'] = True
                        return c
            return {'success': True, 'found': False}
        else:
            return {'success': False}
