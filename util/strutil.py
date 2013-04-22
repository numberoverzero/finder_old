

def sanitize(string):
    '''Returns the string as unicode, with \n line endings'''
    try:
        string = unicode(string, encoding='utf-8')
    except UnicodeEncodeError:
        # Already unicode
        pass
    string = string.replace(u'\r\n', u'\n')
    return string


def until(string, suffix):
    '''Returns the string until the first occurance of suffix'''
    if not suffix:
        return string
    return string.split(suffix)[0]
