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
        # sections = response.xpath('//*[@id="content"]/section[1]/section/div/div/div[2]/div[2]/div').getall()
        # sections.pop(0)
        # sections.pop(-1)
        date = '2.' + re.findall(r'february-(\d+)', response.url)[0]
        for i in range(
                len(response.xpath('//*[@id="content"]/section[1]/section/div/div/div[2]/div[2]/div').getall()) // 2):
            sec_xpath = f'//*[@id="content"]/section[1]/section/div/div/div[2]/div[2]/div[{2 * i}]'
            # sec_xpath = f'//*[@id="content"]/section[1]/section/div/div/div[2]/div[2]/div[2     ]/div[2]/div[1]/div[1]'
            # section = re.sub(r'\s+', '', section)
            # section = re.sub(r'<.+?>', '', section)
            event = response.xpath(sec_xpath + '/div[1]').get()
            n_games = len(response.xpath(sec_xpath + '/div[2]/div').getall())
            for j in range(1, 1 + n_games):
                time = response.xpath(sec_xpath + f'/div[2]/div[{j}]/div[1]').get()
                next_time = response.xpath(sec_xpath + f'/div[2]/div[{min(j + 1, n_games)}]/div[1]').get()
                game = response.xpath(sec_xpath + f'/div[2]/div[{j}]/div[2]').get()
                if self.extract_info(next_time) != '小决赛后' and not re.findall(r'\d', self.extract_info(next_time)):
                    game += self.extract_info(response.xpath(sec_xpath + f'/div[2]/div[{min(j + 1, n_games)}]').get())
                yield {'date': date,
                       'event': self.extract_info(event),
                       'time': self.extract_info(time),
                       'game': self.extract_info(game)}

    def extract_info(self, text):
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'<.+?>', '', text)
        return text
