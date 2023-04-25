import scrapy
import w3lib.html
import ast
from datetime import date

class firstScrap(scrapy.Spider):
    name = "smallScrap"
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

    def parse(self, response):

        testHolder = []
        skimThrough = response.css('#mp-upper')

        for dialog in skimThrough:
            # "Featured article" section
            featuredOutput = dialog.css('#mp-tfa p').getall()
            featuredOutput = w3lib.html.remove_tags(featuredOutput[0]) #Cleans out all links for "Today's featrued article" but not all '\' and other errors
            featuredOutput = featuredOutput.replace('\n','') # Removes "\n" from all of the elements
            featuredOutput = featuredOutput.replace("(Full article...)", '') # Remove "Full artricle ..." from the end of the section; TO-DO: add something here instead, like a link


            # "Did you know" section
            dykOutput = dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[1]/div[2]/ul').getall()
            dykOutput = dykOutput[0].split('\n',1) # Splits the list from being one big list into smaller elements similar to how it is on the website
            for x in range(len(dykOutput)):
                dykOutput[x] = dykOutput[x].replace('\n','')
                dykOutput[x] = w3lib.html.remove_tags(dykOutput[x])

            

            # "In the news" section *Mistake in the jsonl file happening where a break to a new element isn't happening
            # Old Style
            # Using .xpath to prevent pulling unwanted info for this section
            # newsOutput = w3lib.html.remove_tags(str(dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/ul').getall()))
            # newsOutput = ast.literal_eval(newsOutput) # Convert string back to list
            # newsOutput = newsOutput[0].split('\n',1) # Splits the list from being one big list into smaller elements similar to how it is on the website
            # newsOutput = [x.replace('\n','') for x in newsOutput] # Removes "\n" from all of the elements

            # New style
            newsOutput = dialog.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/ul').getall()
            # newsOutput = newsOutput[0].split('<li>',1) # Splits the list from being one big list into smaller elements similar to how it is on the website
            newsOutput = [w3lib.html.remove_tags(newsOutput[x]) for x in range(len(newsOutput))] # Removes all HTML tags from list
            # newsOutput = [x.replace('\n','') for x in newsOutput] # Removes "\n" from all of the elements

            holdvar = 0
            changeNews = newsOutput
            for x in range(newsOutput[0].count("\n")):
                testHolder.append(changeNews[0][0:changeNews[0].index('\n')])
                changeNews = changeNews[0][changeNews[0].index('\n'):]
                # print(testHolder)

                
            # for x in range(len(newsOutput)):
            #     newsOutput[x] = newsOutput[x].replace('\n','')
            #     newsOutput[x] = w3lib.html.remove_tags(newsOutput[x])
            

            
            yield {
                "Today's date": date.today(),
                "Today's featured article": featuredOutput,
                # "Did you know": dykOutput,
                "In the news": testHolder
            }
        
        
