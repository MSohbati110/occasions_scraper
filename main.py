from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.time.ir/fa/eventyear-%D8%AA%D9%82%D9%88%DB%8C%D9%85-%D8%B3%D8%A7%D9%84%DB%8C%D8%A7%D9%86%D9%87').text
soup = BeautifulSoup(html_text, 'lxml')

months_events = soup.find_all('div', class_ = 'eventsCurrentMonthWrapper')
data = [{"model": "date_events.DateEvent", "pk": -1, "fields": {"type": "?????", "date": "?????", "events": [{"importance": "", "text": "?????"}]}}]
counter = 0

fa_months = {
  'فروردین': '01',
  'اردیبهشت': '02',
  'خرداد': '03',
  'تیر': '04',
  'اَمرداد': '05',
  'شهریور': '06',
  'مهر': '07',
  'آبان': '08',
  'آذر': '09',
  'دی': '10',
  'بهمن': '11',
  'اسفند': '12',
}
en_months = {
  'January': '01',
  'February': '02',
  'March': '03',
  'April': '04',
  'May': '05',
  'June': '06',
  'July': '07',
  'August': '08',
  'September': '09',
  'October': '10',
  'November': '11',
  'December': '12',
}
def fa_to_en (fa_text):
  numbers = {
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
  }
  
  en_text = ''
  for i in fa_text:
    en_text += numbers[i]

  if len(en_text) == 1:
    en_text = '0' + en_text

  return en_text

for i in range(12):
  for event in months_events[i].ul.find_all('li'):
    temp = {"model": "date_events.DateEvent", "pk": counter, "fields": {"type": "?????", "date": "?????", "events": [{"importance": "", "text": "?????"}]}}
    event_text = event.text.split()

    if '[' in event_text:
      start_index = event_text.index('[')

      if event_text[start_index+2] in en_months: # ad
        day = event_text[start_index+1]

        if len(day) == 1:
          day = '0' + day
        
        temp["fields"]["type"] = 'ad'
        temp["fields"]["date"] = en_months[event_text[start_index+2]] + '-' + day
        temp["fields"]["events"][0]["text"] = ' '.join(event_text[2:start_index])
      else: # lunar
        temp["fields"]["type"] = 'solar'
        temp["fields"]["date"] = fa_months[event_text[1]] + '-' + fa_to_en(event_text[0])
        temp["fields"]["events"][0]["text"] = ' '.join(event_text[2:start_index])
    else: # solar
      temp["fields"]["type"] = 'solar'
      temp["fields"]["date"] = fa_months[event_text[1]] + '-' + fa_to_en(event_text[0])
      temp["fields"]["events"][0]["text"] = ' '.join(event_text[2:])

    if len(event['class']) == 1:
      temp["fields"]["events"][0]["importance"] = 'Holiday'

    if data[-1]["fields"]["type"] == temp["fields"]["type"] and data[-1]["fields"]["date"] == temp["fields"]["date"]:
      data[-1]["fields"]["events"].append(temp["fields"]["events"][0])
    else:
      data.append(temp)
      counter += 1
data.pop(0)

for item in data:
  print(item)