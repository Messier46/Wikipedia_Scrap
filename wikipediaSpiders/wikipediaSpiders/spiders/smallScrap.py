import scrapy
import w3lib.html
import ast
from datetime import date

class firstScrap(scrapy.Spider):
    name = "smallScrap"
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

    def parse(self, response):

        skimThrough = response.css('#mp-upper')

        for dialog in skimThrough:
            # "Featured article" section
            featuredOutput = w3lib.html.remove_tags(str(dialog.css('#mp-tfa p').getall())) #Cleans out all links for "Today's featrued article" but not all '\' and other errors
            featuredOutput = ast.literal_eval(featuredOutput) # Convert string back to list
            featuredOutput = featuredOutput[0]
            featuredOutput = featuredOutput.replace('\n','') # Removes "\n" from all of the elements


            

            # "In the news" section
            # Using .xpath to prevent pulling unwanted info for this section
            newsOutput = w3lib.html.remove_tags(str(dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/ul').getall()))
            newsOutput = ast.literal_eval(newsOutput) # Convert string back to list
            newsOutput = newsOutput[0].split('\n',1) # Splits the list from being one big list into smaller elements similar to how it is on the website
            newsOutput = [x.replace('\n','') for x in newsOutput] # Removes "\n" from all of the elements
            

            
            yield {
                "Today's date": date.today(),
                "Today's featured article": featuredOutput,
                "In the news": newsOutput
            }
        
        
