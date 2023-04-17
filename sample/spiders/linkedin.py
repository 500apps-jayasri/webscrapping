import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["https://www.linkedin.com/jobs/search?keywords=testing&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"]
    current_page = 0

    def parse(self, response):
        job_links_data = response.xpath("//ul[@class='jobs-search__results-list']/li/div/a").xpath('@href').getall()
        for job_link in job_links_data:
            print("========== ", len(job_links_data), "++++++++", job_links_data)
            yield scrapy.Request(url=job_link, callback=self.parse_job, dont_filter=True)
            
        self.current_page += 1
        next_url = f"https://www.linkedin.com/jobs/search?keywords=testing&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&currentJobId=3564601980"
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)
    
    
    def parse_job(self, response):
        job_dict = {}
        title = response.xpath("//div[@class='top-card-layout__entity-info-container flex flex-wrap papabear:flex-nowrap']/div/h1/text()").get()
        company_name = response.xpath("//div[@class='top-card-layout__entity-info-container flex flex-wrap papabear:flex-nowrap']/div/h4/div/span/a/text()").get()
        location = response.xpath("//h4[@class='top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5']/div[1]/span[2]/text()").get()
        posted_time = response.xpath("//h4[@class='top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5']/div[2]/span[1]/text()").get()
        applications_received = response.xpath("//h4[@class='top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5']/div[2]/span[2]/text()").get()
        job_posting_details = response.xpath("//div[@class='core-section-container__content break-words']/div/section/div/text()").get()
        
        title = title.strip() if title else ''
        company_name = company_name.strip() if company_name else ''
        location = location.strip() if location else ''
        posted_time = posted_time.strip() if posted_time else ''
        
        job_dict = {
           'title': title,
          'company_name': company_name,
          'location': location,
          'posted_time' : posted_time,
          'applications_received' : applications_received,
          'job_posting_details' : job_posting_details
        }
        print(job_dict,"details")
        yield job_dict
        