from urllib.parse import urlparse


def validateUrl(url):
    parsedUrl = urlparse(url)
    return parsedUrl.scheme != '' and parsedUrl.netloc != ''
