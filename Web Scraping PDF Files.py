#WEB SCRAPING PDF FILES 

#Description: This is my first attempt at web scraping using the Requests and 
#Beautiful Soup libraries. The following code is a simple program for accessing 
#the web and extracting links to PDF files from a given web page.


#Importing the Python modules to use 
import requests
from bs4 import BeautifulSoup
import re


#Version 1: 
#For this version, I will search for and extract PDF links from the wikipedia 
#page on 'Memory'. To do so, I will utilize the requests module to access the 
#web page and the beautiful soup library to parse the page and identify the links. 

#First, specifying the url (web address) to the wikipedia page
url = "https://en.wikipedia.org/wiki/Memory"

#making a get request to access web page
page = requests.get(url)

#extracting HTML document
html = page.text

#creating soup object to parse the HTML document
soup = BeautifulSoup(html, 'html.parser')

#to retreive the pdf links (using a regular expression to match with)
pdf_links = soup.find_all(href=re.compile('.+\.pdf'))        #only matches values that end in '.pdf'

#to display the links
for pdf in pdf_links:
    print('link:', pdf.get('href'))
    print('')



#Version 2:
#This version will be similar to before, scraping pdf links from a web page, except this time I will
#make sure to save only those links that are active into a list, and discard those that are not. To do 
#so, I have include two filters, the first makes sure that the pdf link works at all, i.e., the referenced 
#web page in fact exists, meanwhile the second filter makes sure that the link can be accessed given that 
#sometimes a link might reference a web page that exists and yet is inaccessible (this could be due to access 
#being unauthorized or the requested page is not available, despite being active, among others). Finally, this 
#time I'll access another wikipedia page, the page on 'Attention'. 


#Specifying the url (web address) to the wikipedia page
url = "https://en.wikipedia.org/wiki/Attention"

#making a get request to access web page
page = requests.get(url)

#extracting HTML document
html = page.text

#creating soup object to parse the HTML document
soup = BeautifulSoup(html, 'html.parser')

#creating a set object to save active links into
active_links_set = set()

#to retreive the pdf links
pdf_links = soup.find_all(href=re.compile('.+\.pdf'))       # only matches values that end in '.pdf'

#to save only those that are active
for element in pdf_links:
    pdf = element.get('href')     #extract pdf link 
    
    #Filter 1: checking if the referenced web page exists all 
    try: 
        req = requests.get(pdf) 
    except:
        print('Page does not exist:', pdf)
        continue 
        
    #Filter 2: checking the status code to make sure the link is accessible    
    pdf_status_code = requests.get(pdf).status_code
    if pdf_status_code != 200:            # status code != 200 would mean that the web page cannot be accessed (even if the link is active)
        print('Page changed or is not found:', pdf)
        continue
    
    #adding active link to the set
    active_links_set.add(pdf)

print('')

#displaying the active links 
for pdf in active_links_set:
    print('Active link:', pdf)
print('')

#Comparing the number of retrieved pdf links vs. only active links 
print("Total number of all links retrieved:", len(pdf_links))
print('Total number of active links:', len(active_links_set))



#Version 3: 
#This version is more general purpose. It consists of the same code as before, except this time it allows the 
#user to insert any web page they like. More coded was also added to make sure the entered links are valid and/or 
#that they do contain any pdf links. It also filters the links and saves only the active ones. Feel free to try
#it several times on different web pages to scrape pdf links from.

while True:
    #Prompting the user for a url (web address)
    url = input('Enter web address: ')
    
    #Checking if the web page entered exists 
    try:
        #making a get request to access web page
        page = requests.get(url)
        #extracting the HTML document
        html = page.text
    except:
        print('Web Address is incorrect or does not exist. Please try again.')
        continue 


    #Creating soup object to parse the HTML document
    soup = BeautifulSoup(html, 'html.parser')

    #creating a set object to save active links into
    active_links_set = set()


    #Searching for & retreiving pdf links (if any are found)
    pdf_links = soup.find_all(href=re.compile('.+\.pdf'))       #only matches values that end in '.pdf'

    #checking if any pdf links were found
    if len(pdf_links) > 0:
        break           #if yes, breaks from the loop
    else:
        print('Page does not contain any PDF links. Try a different web page.')
        continue 


#Saving only those that are active
for element in pdf_links:
    pdf = element.get('href')     #extract pdf link 
    
    #Filter 1: checking if the referenced web page exists all 
    try: 
        req = requests.get(pdf) 
    except:
        continue 
        
    #Filter 2: checking the status code to make sure the link is accessible    
    pdf_status_code = requests.get(pdf).status_code
    if pdf_status_code != 200:            # status code != 200 would mean that the web page cannot be accessed (even if the link is active)
        continue
    
    #adding active link to the set
    active_links_set.add(pdf)


#Displaying the retrieved pdf links 
for pdf in active_links_set:
    print('Link:', pdf)

#displaying the number of pdf links retrieved 
print('\nTotal number of active pdf links retrieved:', len(active_links_set))
