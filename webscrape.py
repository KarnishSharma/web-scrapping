import urllib
import urllib.request
from bs4 import BeautifulSoup #use as parser for scrapping
from random import choice #random choice
import requests  # FOr HTTP requests
import pyfiglet  #for ASCII ART
from time import sleep

base_url="http://quotes.toscrape.com"

def scrape_quote():
   all_quotes=[]
   pg_url="/page/1"
   while pg_url:

      r1=requests.get(f"{base_url}{pg_url}",headers={"Accept":"text/plain"})
      print(f"Now scrapping  {base_url}{pg_url}........\n" )
       #will give us page number #print(r1.text) #code to get any single quote

      s1=BeautifulSoup(r1.text,"html.parser")
      #s2=s1.find_all(attrs={"itemprop":"text"})[1] #just use first item of list having all quotes of the page
         # print(s2.get_text()) #get_text return only the text
      #find the class name quote.This having all the quotes and author details
      quotes=s1.find_all(class_="quote")
      #print(quotes)   #return a list     #now loop thorugh all the Quotes and print quote and author
      #now class text conatin the Quote,author class has author name and href link about the author
      #print(s1.get_text()) ,get_text() not works with find_all
      
      #let store all in a list  all_quotes[]
      #also we have to find the link about the author ....
      #that can be find using attribute finding
      #x.find(tag)[attribute]  ,retturn first href (as use find)
      for quote in quotes:

         all_quotes.append({"text":(quote.find(class_="text")).get_text(),
            "author":quote.find(class_="author").get_text(),
            "bio_data":quote.find("a")["href"]
            })
            #print((quote.find(class_="text")).get_text())  #print(quote.find(class_="author").get_text())


      #now check the next button....it has class name next. and we require the href
      nxt_btn=s1.find(class_="next")

      pg_url=nxt_btn.find("a")["href"]  if nxt_btn else None
      #if nxt_btn exist than store to page url other wise exit while loop
      sleep(1)
      #time of 2 sec before every page scrapped otherwise you may be problem

   return all_quotes
    

def start_game(quotes):

   description=''
   #use choice to select a random quote 
   #all_quotes is a list that have dictionary as elements having text,author,bio_data
   r_quote=choice(quotes)  #now print text of the quote
   print(f"{r_quote['author']}\n\n")

   print("Guess the Author of the quote.....\n\n")
   #print("Here is the quote.....")
   print(r_quote["text"])
   rm_gs=4
   gs=''
   #use .lower() so that no problem whatever user write
   while gs.lower() != r_quote["author"].lower() and rm_gs > 0 :

      gs=input(f"Remaining guesses are {rm_gs} \n")
      rm_gs -= 1 
      res=requests.get(f"{base_url}{r_quote['bio_data']}")
      s2=BeautifulSoup(res.text,"html.parser")
      description=s2.find(class_="author-description").get_text()

      if gs.lower() == r_quote["author"].lower():
         x="You Won..."
         print(pyfiglet.figlet_format(x))
         print("You Get it!!!!\n Congratulations...")
         break
         
      if rm_gs==3:
         #we have to give hint to user....from the bio_data link....we have to scrap  the  description page...
         #make a request to this page and then store in beautiful soup object...
         birth_date=s2.find(class_="author-born-date").get_text()
         birth_place=s2.find(class_="author-born-location").get_text()
         print(f"There is an Hint --> Author born on {birth_date} in {birth_place}")

      elif rm_gs==2:
         print(f"There is an Hint --> Author first name start with {r_quote['author'][0]}")

      elif rm_gs==1:
         last=r_quote['author'].split(" ")[1][0] #split from space and print first letter of the lastname last=[mohit,rohilla]
         print(f"There is an Hint --> Author last name start with {last}")

      else:
         y=f"OOps !! You lost.\n Answer is\n {r_quote['author']}"
         print(pyfiglet.figlet_format(y))
         print(f"You are ran out of guesses and the answer is [{r_quote['author']}]  and some description about the author is..")

   print(description)

   #now for play again manner of game...
   again=''
   while again.lower() not in ('yes','y','no','n'):

      again=input("Want to play again (y/n)?")

   if again.lower() in ('yes','y'):

      print("Play again.......\n\n")
      return start_game(quotes)
      
   else:
      print("\n\n ok bye, see you next time!!!!")
         

quotes=scrape_quote() #list of all quotes

start_game(quotes)
