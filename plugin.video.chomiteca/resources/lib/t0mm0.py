import urllib
import gzip
import io
import os
import re
import xbmc
import xbmcaddon
import pickle
import http.cookiejar as cookielib
import cgi

class Net:
    _cj = cookielib.LWPCookieJar()
    _proxy = None
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'

    def __init__(self, cookie_file='', proxy='', user_agent='', 
                 http_debug=False):
                self._http_debug = http_debug
                self._update_opener()

    def http_POST(self, url, form_data, headers={}, compression=True):
        '''
        Perform an HTTP POST request.
        
        Args:
            url (str): The URL to POST.
            
            form_data (dict): A dictionary of form data to POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        return self._fetch(url, form_data, headers=headers,
                           compression=compression)
    
    def _fetch(self, url, form_data={}, headers={}, compression=True):
        '''
        Perform an HTTP GET or POST request.
        
        Args:
            url (str): The URL to GET or POST.
            
            form_data (dict): A dictionary of form data to POST. If empty, the 
            request will be a GET, if it contains form data it will be a POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        encoding = ''
        req = urllib.request.Request(url)
        if form_data:
            form_data = urllib.parse.urlencode(form_data).encode("utf-8")
            req = urllib.request.Request(url, form_data)
        req.add_header('User-Agent', self._user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        response = urllib.request.urlopen(req)
        return HttpResponse(response)
    
    def save_cookies(self, cookie_file):
        '''
        Saves cookies to a file.
        
        Args:
            cookie_file (str): Full path to a file to save cookies to.
        '''
        self._cj.save(cookie_file, ignore_discard=True)     
    
    def set_cookies(self, cookie_file):
        '''
        Set the cookie file and try to load cookies from it if it exists.
        
        Args:
            cookie_file (str): Full path to a file to be used to load and save
            cookies to.
        '''
        try:
            self._cj.load(cookie_file, ignore_discard=True)
            self._update_opener()
            return True
        except:
            return False
    
    def _update_opener(self):
        '''
        Builds and installs a new opener to be used by all future calls to 
        :func:`urllib2.urlopen`.
        '''
        if self._http_debug:
            http = urllib.request.HTTPHandler(debuglevel=1)
        else:
            http = urllib.request.HTTPHandler()
            
        if self._proxy:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cj),
                                          urllib.request.ProxyHandler({'http': 
                                                                self._proxy}), 
                                          urllib.request.HTTPBasicAuthHandler(),
                                          http)
        
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cj),
                                          urllib.request.HTTPBasicAuthHandler(),
                                          http)
        urllib.request.install_opener(opener)


class HttpResponse:
    '''
    This class represents a response from an HTTP request.
    
    The content is examined and every attempt is made to properly encode it to
    Unicode.
    
    .. seealso::
        :meth:`Net.http_GET`, :meth:`Net.http_HEAD` and :meth:`Net.http_POST` 
    '''
    
    content = ''
    '''Unicode encoded string containing the body of the response.'''
    
    
    def __init__(self, response):
        '''
        Args:
            response (:class:`mimetools.Message`): The object returned by a call
            to :func:`urllib2.urlopen`.
        '''
    
        self._response = response
        html = response.read()
        try:
            if response.headers['content-encoding'].lower() == 'gzip':
                html = gzip.decompress(html).decode()
        except:
            pass
        
        try:
            content_type = response.headers['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass
            
        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', html, re.IGNORECASE)
        if r:
            encoding = r.group(1) 
                   
        try:
            html = str(html, encoding)
        except:
            pass
            
        self.content = html
    
    
    def get_headers(self):
        '''Returns a List of headers returned by the server.'''
        return self._response.info().headers
    
        
    def get_url(self):
        '''
        Return the URL of the resource retrieved, commonly used to determine if 
        a redirect was followed.
        '''
        return self._response.geturl()

class Addon():
    def __init__(self, addon_id, argv=None):
        '''        
        Args:
            addon_id (str): Your addon's id (eg. 'plugin.video.t0mm0.test').
            
        Kwargs:
            argv (list): List of arguments passed to your addon if applicable
            (eg. sys.argv).
        '''
        self.addon = xbmcaddon.Addon(id=addon_id)
        if argv:
            self.url = argv[0]
            self.handle = int(argv[1])
            self.queries = self.parse_query(argv[2][1:])
    
    def parse_query(self, query, defaults={'mode': 'main'}):
        '''
        Parse a query string as used in a URL or passed to your addon by XBMC.
        
        Example:
         
        >>> addon.parse_query('name=test&type=basic')
        {'mode': 'main', 'name': 'test', 'type': 'basic'} 
            
        Args:
            query (str): A query string.
            
        Kwargs:
            defaults (dict): A dictionary containing key/value pairs parsed 
            from the query string. If a key is repeated in the query string
            its value will be a list containing all of that keys values.  
        '''
        queries = cgi.parse_qs(query)
        q = defaults
        for key, value in queries.items():
            if len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q
    
    def get_profile(self):    
        '''
        Returns the full path to the addon profile directory 
        (useful for storing files needed by the addon such as cookies).
        '''
        return xbmc.translatePath(self.addon.getAddonInfo('profile'))

    def load_data(self,filename):
        '''
        Load the data that was saved with save_data() and returns the
        data structure.
        
        Args:
            filename (string): Name of the file you want to load data from. This
            file will be loaded from your addons profile directory.
            
        Returns:
            Data structure on success
            False on failure
        '''
        profile_path = self.get_profile()
        load_path = os.path.join(profile_path, filename)
        print(profile_path)
        if not os.path.isfile(load_path):
            self.log_debug('%s does not exist' % load_path)
            return False
        try:
            data = pickle.load(open(load_path))
        except:
            return False
        return data
    
    def save_data(self, filename, data):
        '''
        Saves the data structure using pickle. If the addon data path does 
        not exist it will be automatically created. This save function has
        the same restrictions as the pickle module.
        
        Args:
            filename (string): name of the file you want to save data to. This 
            file will be saved in your addon's profile directory.
            
            data (data object/string): you want to save.
            
        Returns:
            True on success
            False on failure
        '''
        profile_path = self.get_profile()
        os.makedirs(profile_path, exist_ok=True)
        save_path = os.path.join(profile_path, filename)
        try:
            pickle.dump(data, open(save_path, 'wb'))
            return True
        except pickle.PickleError:
            return False

    def log_debug(self, msg):
        '''
        Convenience method to write to the XBMC log file at the 
        ``xbmc.LOGDEBUG`` error level. Use this when you want to print out lots 
        of detailed information that is only usefull for debugging. This will 
        show up in the log only when debugging is enabled in the XBMC settings,
        and will be prefixed with 'DEBUG:'.
        '''
        self.log(msg, xbmc.LOGDEBUG)    
    
    def log(self, msg, level=xbmc.LOGINFO):
        '''
        Writes a string to the XBMC log file. The addon name is inserted into 
        the beginning of the message automatically to help you find relevent 
        messages in the log file.
        
        The available log levels are defined in the :mod:`xbmc` module and are
        currently as follows::
        
            xbmc.LOGDEBUG = 0
            xbmc.LOGERROR = 4
            xbmc.LOGFATAL = 6
            xbmc.LOGINFO = 1
            xbmc.LOGNONE = 7
            xbmc.LOGNOTICE = 2
            xbmc.LOGSEVERE = 5
            xbmc.LOGWARNING = 3
        
        Args:
            msg (str or unicode): The message to be written to the log file.
        
        Kwargs:
            level (int): The XBMC log level to write at.
        '''
        #msg = unicodedata.normalize('NFKD', unicode(msg)).encode('ascii',
        #                                                         'ignore')
        xbmc.log(f'{(self.get_name(), msg)}: {level}')
