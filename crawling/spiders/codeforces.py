from scrapy import Spider, Request
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
                name =  response.css(f'.standings tr[participantid="{id}"] a.rated-user::attr(href)').get().replace("/profile/", "")
                score =  response.css(f'.standings tr[participantid="{id}"] span[title="Score"]::text').get().replace(f"\r", "").replace("\n", "").replace(" ", "")
                if country == 'China':
                    user.append( [country, name, score] ) 
                    data[id] = [ name, score ]
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
            

