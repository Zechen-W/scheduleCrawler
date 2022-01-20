import scrapy
import re


class WzcSpider(scrapy.Spider):
    name = "wzc_spider"

    # start_urls = ['https://www.beijing2022.cn/cn/schedule/index.htm#']
    def start_requests(self):
        urls = []
        for day in range(2, 21):
            urls.append(f"https://olympics.com/zh/beijing-2022/schedule-by-day/february-{day}/")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date = '2.' + response.url[62:-1]
        base = '//*[@id="content"]/section/div/div/section/div/div/div[2]/div[2]/div'
        n_event = (len(response.xpath(
            '//*[@id="content"]/section/div/div/section/div/div/div[2]/div[2]/div').getall()) - 2) // 2

        for i_event in range(n_event):
            base_event = f'//*[@id="content"]/section/div/div/section/div/div/div[2]/div[2]/div[{i_event * 2 + 2}]'
            event = response.xpath(f'{base_event}/div[1]/div/div[2]/label').re(r'<label>(.*)</label>')[0]

            base_line = f'{base_event}/div[2]/div'
            n_line = len(response.xpath(base_line).getall())
            items = []
            for i_line in range(n_line):
                base_line = f'{base_event}/div[2]/div[{i_line + 1}]'
                n_col = len(response.xpath(f'{base_line}/div').getall())
                if n_col == 2:
                    time = response.xpath(f'{base_line}/div[1]/label').re(r'<label>(.*)</label>')
                    time = ''.join(time)
                    game = response.xpath(f'{base_line}/div[2]/label').re(r'<label>(.*)</label>')
                    game = ''.join(game)
                    items.append({'date': date,
                                  'event': event,
                                  'time': time,
                                  'game': game})

                elif n_col == 3:
                    # raise Exception('this is n_col==3')
                    ctry1 = response.xpath(f'{base_line}/div[1]/div[2]/span').re(r'<span>(.*)</span>')[0].strip()
                    ctry2 = response.xpath(f'{base_line}/div[3]/div[1]/span').re(r'<span>(.*)</span>')[0].strip()
                    items[-1]['game'] = items[-1]['game'] + f'; {ctry1} VS {ctry2}'

            for item in items:
                yield item

    def extract_info(self, text):
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'<.+?>', '', text)
        return text
