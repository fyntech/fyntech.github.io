from bs4 import BeautifulSoup
from datetime import datetime
import requests
import locale

# Use danish month names
locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

page_link ='https://www.prosa.dk/nc/arrangementer/?tx_news_pi1[overwriteDemand][locations][2]=Fyn'
page_response = requests.get(page_link, timeout=20)
page_content = BeautifulSoup(page_response.content, 'html.parser')

# extract all html elements where price is stored
events = page_content.find_all(class_='article')

for event in page_content.find_all(class_='article'):
  # title 
  eventTitle = event.find('span', itemprop='headline').text
  if eventTitle.startswith('Odense: '):
    title = eventTitle[8:]
  else:
    title = eventTitle
  #print(title)

  # dateStart / Y-m-d H:i:s Europe/Copenhagen
  eventDate = event.find(class_='news-list-date')
  eventDateDay = eventDate.find(class_='day').text.strip('.')
  eventDateMonth = eventDate.find(class_='month').text
  eventDateYear = eventDate.find(class_='year').text
  eventDateTime = eventDate.find(class_='eventTime').text
  date = ''.join([eventDateYear, ' ', eventDateMonth, ' ', eventDateDay, ' ', eventDateTime])
  date = datetime.strptime(date, '%Y %B %d %H:%M')
  dateStart = ' '.join([date.strftime('%Y-%m-%d %H:%M:%S'), 'Europe/Copenhagen'])
  #print(dateStart)

  # location
  eventLocation = event.find(class_='arrangement-address').text
  location = ' '.join(eventLocation.split())
  #print(location)

  # link
  eventLink = event.find('a', href=True)
  link = ''.join(['https://www.prosa.dk/', eventLink['href']])
  #print(link)

  # description
  eventDescription = event.find('div', itemprop='description').text
  description = eventDescription
  #print(description)

  # filename / date-title.md
  filenameDate = date.strftime('%Y-%m-%d')
  filenameTitle = title.replace(' ', '-')
  filenameTitle = filenameTitle.replace('.','')
  filename = ''.join([filenameDate, '-', filenameTitle.lower(), '.md'])
  filepath = '_events/' + filename

  with open(filepath, 'w') as f:
    f.write('---\n')
    f.write('title: "' + title + '"\n')
    f.write('dateStart: "' + dateStart + '"\n')
    f.write('location: "' + location + '"\n')
    f.write('link: "' + link + '"\n')
    f.write('organizer: "PROSA"\n')
    f.write('category: "prosa"\n')
    f.write('---\n')
    f.write(description + '\n')
