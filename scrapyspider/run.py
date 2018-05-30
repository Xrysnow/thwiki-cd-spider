from scrapy import cmdline

name = 'myspider'
cmd = 'scrapy crawl {0} --loglevel=WARNING'.format(name)
print('start cmdline...')
cmdline.execute(cmd.split())
