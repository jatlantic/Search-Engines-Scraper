from ..engine import SearchEngine
from ..config import PROXY, TIMEOUT, FAKE_USER_AGENT


class Bing(SearchEngine):
    '''Searches bing.com'''
    def __init__(self, proxy=PROXY, timeout=TIMEOUT):
        super(Bing, self).__init__(proxy, timeout)
        self._base_url = u'https://www.bing.com'
        self.set_headers({'User-Agent':FAKE_USER_AGENT})

    # new
        
    def _selectors_ads(self, element):
        '''Returns the appropriate CSS selector for ad results.'''
        selectors = {
            'url': '.sb_add .b_adurl cite', 
            'title': '.sb_add h2',
            'text': '.sb_add .b_ad_description', 
            'links': '.sb_add', 
            'next': 'div#b_content nav[role="navigation"] a.sb_pagN'
        }
        return selectors[element]

    def _selectors(self, element):
        '''Returns the appropriate CSS selector.'''
        selectors = {
            'url': 'div.b_attribution cite', 
            'title': 'h2', 
            'text': 'p', 
            'links': 'ol#b_results > li.b_algo', 
            'next': 'div#b_content nav[role="navigation"] a.sb_pagN'
        }
        return selectors[element]
    
    def _first_page(self):
        '''Returns the initial page and query.'''
        self._get_page(self._base_url)
        url = u'{}/search?q={}&search=&form=QBLH'.format(self._base_url, self._query)
        return {'url':url, 'data':None}
    
    def _next_page(self, tags):
        '''Returns the next page URL and post data (if any)'''
        selector = self._selectors('next')
        next_page = self._get_tag_item(tags.select_one(selector), 'href')
        url = None
        if next_page:
            url = (self._base_url + next_page) 
        return {'url':url, 'data':None}

    def _get_url(self, tag, item='href'):
        '''Returns the URL of search results items.'''
        return super(Bing, self)._get_url(tag, 'text')
