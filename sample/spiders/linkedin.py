import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["https://www.linkedin.com/jobs/search?keywords=testing&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"]

    def parse(self, response):
        # print(response.text)
        job_links_data = response.xpath("//ul[@class='jobs-search__results-list']/li/div/a").xpath('@href').getall()
        
        for job_link in job_links_data:
            yield scrapy.Request(url=job_link, callback=self.parse_job, dont_filter=True)
    
    
    def parse_job(self, response):
        print(response.text)
        job_dict = {}
        title = response.xpath("//div[@class='top-card-layout__entity-info-container flex flex-wrap papabear:flex-nowrap']/div/h1/text()").get()
        job_dict['title'] = title
        yield job_dict
