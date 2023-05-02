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
            featuredOutput = dialog.css('#mp-tfa p').getall()
            featuredOutput = w3lib.html.remove_tags(featuredOutput[0]) #Cleans out all links for "Today's featrued article" but not all '\' and other errors
            featuredOutput = featuredOutput.replace('\n','') # Removes "\n" from all of the elements
            featuredOutput = featuredOutput.replace("(Full article...)", '') # Remove "Full artricle ..." from the end of the section; TO-DO: add something here instead, like a link


            # "Did you know" section
            dykOutput = dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[1]/div[2]/ul').getall()
            dykOutput = [w3lib.html.remove_tags(dykOutput[x]) for x in range(len(dykOutput))] # Removes all HTML tags from list

            dykOutput = dykOutput[0] # Converts it to a string to allow for '\n' to be removed
            dykOutput = dykOutput.split('\n') # Removes "\n" from all of the elements and returns it to a list
            

            # "In the news" section 
            newsOutput = dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/ul').getall()
            newsOutput = [w3lib.html.remove_tags(newsOutput[x]) for x in range(len(newsOutput))] # Removes all HTML tags from list
            newsOutput = newsOutput[0] # Converts it to a string to allow for '\n' to be removed
            newsOutput = newsOutput.split('\n') # Removes "\n" from all of the elements and returns it to a list

            # "On this day" section
            dayOutput = dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[2]/div[2]/ul').getall()
            dayOutput = w3lib.html.remove_tags(dayOutput[0])
            dayOutput = dayOutput.split('\n')
            
            yield {
                "Today's date": date.today(),
                "Today's featured article": featuredOutput,
                "Did you know": dykOutput,
                "In the news": newsOutput,
                "On this day": dayOutput
            }
        
        
