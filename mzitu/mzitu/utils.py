import platform

def downloadPath():
    if 'Windows' == platform.system():
        return 'D:/scrapy/Spiders/mzitu/mzitu/test/'
    else:
        return '/Users/UndCover/Desktop/Spider/Spiders/mzitu/test/'