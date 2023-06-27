from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import json


class Codeforces(Spider):
    name = "codeforces"
    allowed_domains = ["codeforces.com"]
    start_urls = ["https://codeforces.com/contest/1842/standings/page/1"]

    def parse(self, response):
        json_file_path = r'C:\Users\ADMIN\Projects\Django\crawling\codeforces.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data = {}
        else:
            data = {}
        user = []
        participantid = response.css('tr::attr(participantid)').getall()
        for id in participantid:

            try:
                country = response.css(f'.standings tr[participantid="{id}"] img::attr(title)').get()
                name = response.css(f'.standings tr[participantid="{id}"] a.rated-user::attr(href)').get().replace(
                    "/profile/", "")
                score = response.css(f'.standings tr[participantid="{id}"] span[title="Score"]::text').get().replace(
                    f"\r", "").replace("\n", "").replace(" ", "")
                if country == 'China':
                    user.append([country, name, score])
                    data[id] = [name, score]
            except:
                pass

        with open(json_file_path, 'w') as f:
            json.dump(data, f)

        yield {
            "user": user
        }

        for page in range(2, 92):
            url = f"https://codeforces.com/contest/1842/standings/page/{page}"
            yield Request(url, callback=self.parse)


class SubmissionsSpider(Spider):
    name = "submissions"
    allowed_domains = ["codeforces.com"]
    start_urls = ["https://codeforces.com/submissions/Ignr_h31/page/1"]

    def parse(self, response):
        submissions_id = response.css('tr::attr(data-submission-id)').getall()
        problems = [
            x.replace(' ', '').replace('\r', '').replace('\n', '') for x in response.css('tr td a[href*=problem]::text').getall()]
        verdicts = []
        submissions_url = ['https://codeforces.com' + x for x in response.css('tr td a[href*=problem]::attr(href)').getall()]
        for id in submissions_id:
            verdicts.append(
                response.css(f'span.submissionVerdictWrapper[submissionid="{id}"] span.verdict-accepted::text').get())
        datas = []
        for i in range(len(verdicts)):
            if verdicts[i] == 'Accepted':
                submissions_url[i] = submissions_url[i].replace('problem', 'submission')[:-1] + submissions_id[i]
                datas.append([ problems[i], submissions_url[i] ])
        
        for [name, url] in datas:
            print(name, url)
            yield Request(url=url, callback=self.parse_specific_submission, meta={'name': name})
            #response.css('#program-source-text::text').getall()

        for page in range(2, 13):
            url = f"https://codeforces.com/submissions/Ignr_h31/page/{page}"
            yield Request(url=url, callback=self.parse)
    
    def parse_specific_submission(self, response):
        name = response.meta['name']
        try:
            program_source = response.css('#program-source-text::text').get().replace('\n', '')
            filename = name + ".cpp"
            foldername = "Submissons Codeforces"
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            filepath = os.path.join(foldername, filename)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(program_source)
        except: 
            pass

        
        
        
            


