# -*- coding: utf-8 -*-
import scrapy
#from scrapy import Request
#from scrapy.selector import Selector
from scrapyspider.items import MyspiderItem
Request = scrapy.Request
Selector = scrapy.selector.Selector
#Response = scrapy.responsetypes.Response

class MySpider(scrapy.spiders.Spider):
    name = 'myspider'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
        /537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', }
    types = {'infoRD': 'vocal', 'infoYD': 'instrumental',
             'infoRL': 'original_vocal', 'infoYL': 'original_instrumental',
             'infoO': 'cover'}
    infotypes = {'编曲': 'arrange', '演唱': 'vocal', '作词': 'lyric'}
    domain = 'http://thwiki.cc/'
    start = 'http://thwiki.cc/同人社团列表'
    #start = 'http://thwiki.cc/IOSYS'
    
    def start_requests(self):
        yield Request(self.start, headers=self.headers, callback=self.parse)

    def parse(self, response):
        t1 = response.xpath(
            '//div[@class="page-content-header circle"]/div/b/text()').extract()
        t2 = response.xpath(
            '//div[@class="page-content-header album-type doujin-album"]/div/b/a/text()').extract()
        if len(t1) > 0:
            if t1[0] == '同人社团':
                se = response.xpath(
                    '//table[@class="doujinworklist"]/tbody/tr/td/b/a').extract()
                if len(se) > 0:
                    for s in se:
                        se2 = Selector(text=s)
                        try:
                            album_name = se2.xpath('//a/text()').extract()[0]
                            album_url = se2.xpath('//a/@href').extract()[0]
                            url = self.domain[:-1] + album_url
                            yield Request(url, headers=self.headers, callback=self.parse, meta={'society':response.meta['society'], 'album':album_name})
                        except:
                            pass
        elif len(t2) > 0:
            if t2[0] == '二次同人音乐':
                item = MyspiderItem()
                tracks = response.xpath(
                    '//table[@class="wikitable musicTable"]/tr').extract()
                if len(tracks) == 0:
                    return
                ind = []
                for i in range(len(tracks)):
                    id = Selector(text=tracks[i]).xpath(
                        '//td/b/text()').extract()
                    if len(id) > 0:
                        ind.append(i)
                ind.append(len(tracks))
                for i in range(len(ind) - 1):
                    trackinfo = tracks[ind[i]:ind[i + 1]]
                    item['idx'] = str(i+1)
                    item['society'] = response.meta['society']
                    item['album'] = response.meta['album']
                    self.parseinfo(item, trackinfo)
                    yield item
        else:
            se=response.xpath('//td[@class="社团名 smwtype_wpg"]/a').extract()
            if len(se)>0:
                try:
                    for s in se:
                        se2 = Selector(text=s)
                        society_name = se2.xpath('//a/text()').extract()[0]
                        society_url = se2.xpath('//a/@href').extract()[0]
                        url = self.domain[:-1] + society_url
                        yield Request(url, headers=self.headers, callback=self.parse, meta={'society':society_name})
                except:
                    pass

    def parseinfo(self, item, infos):
        inf = {'title': '', 'arrange': '', 'vocal': '', 'lyric': '',
               'ogmusic': '', 'source': '', 'ttype': '', 'length': ''}
        rearrange = ''
        for k in inf:
            inf[k] = '_null_'
        for i in range(len(infos)):
            se = Selector(text=infos[i])
            typ = se.xpath('//td[@class="label"]/text()').extract()
            if len(typ) == 0:
                binfos = se.xpath('//td').extract()
                if len(binfos) == 0:
                    pass
                else:
                    for binfo in binfos:
                        se2 = Selector(text=binfo)
                        try:
                            cl = se2.xpath('//td/@class').extract()[0]
                            if cl in self.types:
                                inf['ttype'] = self.types[cl]
                            elif cl == 'title':
                                inf['title'] = se2.xpath(
                                    '//td/text()').extract()[0]
                            elif cl == 'time':
                                inf['length'] = se2.xpath(
                                    '//td/text()').extract()[0]
                        except:
                            pass
            else:
                typ = typ[0]
                try:
                    if typ in self.infotypes:
                        ifs = se.xpath(
                            '//td[@class="text"]/a/text()').extract()
                        if len(ifs)>0:
                            inf[self.infotypes[typ]] = '，'.join(ifs)
                    elif typ == '原曲':
                        ogs = se.xpath(
                            '//td/div[@class="ogmusic"]/a/text()').extract()
                        srs = se.xpath(
                            '//td/div[@class="source"]/a/text()').extract()
                        if len(ogs)>0:
                            inf['ogmusic'] = '|'.join(ogs)
                        if len(srs)>0:
                            inf['source'] = '|'.join(srs)
                    elif typ == '再编曲':
                        inf['ttype'] = 'cover'
                        rearrange = se.xpath(
                            '//td[@class="text"]/a/text()').extract()[0]
                    elif typ == '初发布' or typ == '社团':
                        inf['ttype'] = 'cover'
                except:
                    pass
        if rearrange != '':
            add = '' if inf['arrange']=='_null_' else ' [原编曲：' + inf['arrange'] + ']'
            inf['arrange'] = rearrange + add
        for k in inf:
            item[k] = inf[k]
        return
