from bs4 import BeautifulSoup
from codecs import open
from datetime import datetime
import requests
import time, sched
import urllib.request

from modules.scrape_constants import TVINNA, FILE_LOGS, FILE_CURR
from modules.list_utils import listDiff

# TODO: Fix BUG: The list entries are not always unique. E.g. now (03.12.19) there are two 'Forritari' entries. Make unique!
# TODO: Create constants where applicable.

def scrape(url, scheduler):
    # Read from currentNewJobs.txt - Gets list of all new jobs since last scrape.
    lastScrapeEntries = readFromFile(FILE_CURR)
    
    # Scrape for the newest job ad entries.
    response = requests.get(url)
    parsedResponse =  BeautifulSoup(response.text, 'html.parser')
    
    # The list that interests us is the fourth one of the desktop version of Tvinna.
    entries = parsedResponse.find_all('ul')[3].find_all('li')
    entryNames = [i.find_next('h2').get_text() for i in entries]

    # Jobs that are uncommon among the lists must be new entries.
    # If there are no uncommon jobs, there must be no new entries.
    numNewEntries = len(listDiff(lastScrapeEntries, entryNames))

    if numNewEntries != 0:
        # The new entries are the numNewEntries first ones.
        newEntriesFull = [(i.find_next('p').get_text().split('|')[0].strip(),               # Employer
                        i.find_next('h2').get_text(),                                       # Job title
                        i.find_next('a').get('href')) for i in entries[:numNewEntries]]     # URL
        notify(buildNotification(newEntriesFull), (numNewEntries > 1))
        writeToFile(FILE_CURR, entryNames)
        log(newEntriesFull)
    else:
        log('No new job entries found.')

    scheduler.enter(7200, 1, scrape, argument=(url, scheduler, ))

# Logs to logs.txt: '[TIMESTAMP] - What happened.
def log(dataToLog):
    timeStamp = '[' + datetime.now(tz=None).strftime('%d-%m-%Y (%H:%M:%S)') + ']'

    if type(dataToLog) == list:
        jobs = '['
        for i, job in enumerate(dataToLog):
            print(i, job)
            jobs += job[0] + '->' + job[1] + ('' if (i == (len(dataToLog) - 1)) else ', ')

        jobs += ']'
        writeToFile(FILE_LOGS, timeStamp + ' - New jobs: '  + jobs)
    else:
        writeToFile(FILE_LOGS, timeStamp + ' - '  + dataToLog)

# TODO: Beautify the notification with some HTML.
def buildNotification(newEntries):
    notification = 'Hi!\nTvinna just added the following job advertisement' + ('' if (len(newEntries) == 1) else 's') + ':\n\n'

    for e in newEntries:
        notification += 'Employer: ' + e[0] + '\nJob title: ' + e[1] + '\nLink: ' + e[2] + '\n\n'

    return notification + '\nRegards from the Tvinna monitor!'

# TODO: Throw error if incorrect filename
# Returns file contents as a list of strings.
def readFromFile(file):
    if file == FILE_CURR:
        f = open(file, 'r', encoding='utf-8')
        data = f.read()
        f.close()

        entryData = data.split('\n')
        
        # Empty file.
        if entryData[0] == '':
            return []
        else:
            return entryData

# TODO: Throw error if incorrect filename
# Expects a list of strings which will be written to a file, newline separated.
def writeToFile(file, dataToWrite):
    if file == FILE_CURR:
        sep = '\n'

        f = open(file, 'w', encoding='utf-8')
        f.write(sep.join(dataToWrite))
        f.close()
    elif file == FILE_LOGS:
        f = open(file, 'a', encoding='utf-8')
        f.write(dataToWrite + '\n')
        f.close()

def notify(notification, multi):
    # TODO: Instead of this print statement the info should be logged!
    # print('New job found!\nProvider: ' + job[1] + '\nTitle: ' + job[0] + '\nLink: ' + job[2])
    response = requests.post(
        # NOTE: Contact me, Smári, if you want to try out the e-mail functionality. Otherwise, view logs.txt to check if there are any new job entries.
		'<Mailgun URL/>',
		auth=('api', '<Mailgun key/>'),
		data={'from': 'Tvinna monitor <Mailgun mail address/>',
			'to': ['<Some other mail address/'],
			'subject': 'New job' + ('s' if multi else '') + ' found at Tvinna!',
			'text': notification})

    print(response.text)

def main(url):
    # TODO: Errorcheck if .txt files exist.

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, scrape, argument=(url, scheduler, ))
    scheduler.run()

main(TVINNA)