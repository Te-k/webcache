from urllib.parse import urlparse, parse_qs


def same_url(url1, url2):
    """
    Check for minor differences between url1 and url2, return True if they are the same
    Currently only consider extra www. in domain, https/http and extra fragment
    """
    if url1 == url2:
        return True
    # Dirty hacks
    if not url1.startswith('http'):
        url1 = 'http://' + url1
    if not url2.startswith('http'):
        url2 = 'http://' + url2
    if not url1.endswith('/'):
        url1 += '/'
    if not url2.endswith('/'):
        url2 += '/'
    purl2 = urlparse(url2)
    purl1 = urlparse(url1)

    if purl1.path == purl2.path and purl1.params == purl2.params and \
            purl1.query == purl2.query:
        if purl1.netloc == purl2.netloc:
            return True
        else:
            if ("www." + purl1.netloc) == purl2.netloc:
                return True
            if ("www." + purl2.netloc) == purl1.netloc:
                return True
    return False

