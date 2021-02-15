# Sentiment-Analysis-on-Weibo
This project would crawl the users' comments in Weibo (the Twitter in China ) and complete sentiment analysis on these comments

Run the UI_2.py to run the code.

Since the html of website ended with cn would change; When there is error "Error: list index out of range"
It is required for us to change "div = info.body.find_all("span",class_="txt")" to "div = info.body.find_all("span",class_="ctt")" in the function get_comment of Class Pach in pachong.p




Utilize PM to crawl as follows:

    def get_publish_time(self,info):
        try:
            final_time = []
            str_time = info.body.find_all("div",class_="content")
            for i in str_time:
                t = i.find_all("p",class_="from")
                t = t[-1]
                b=''
                for word in t.text:
                    if word != ' ' and word != '\n':
                        b += word
                publish_time = b.split('\xa0')[0]
                print(publish_time)
                if '刚刚' in publish_time:
                    publish_time = datetime.now().strftime('%Y-%m-%d% H:%M')
                elif '分钟' in publish_time:
                    minute = publish_time[:publish_time.find('分钟')]
                    minute = timedelta(minutes=int(minute))
                    publish_time = (datetime.now() - minute).strftime('%Y-%m-%d% H:%M')
                elif '今天' in publish_time:
                    today = datetime.now().strftime('%Y-%m-%d')
                    time = publish_time[3:]
                    publish_time = today + ' ' + time
                elif '月' in publish_time:
                    year = datetime.now().strftime('%Y')
                    month = publish_time[0:2]
                    day = publish_time[3:5]
                    time = publish_time[6:11]
                    publish_time = year + '-' + month + '-' + day + ' ' + time
                final_time.append(publish_time[0:10])
            return final_time
        except Exception as e:
            print('Error:',e)


Utilize PC to crawl as follows:

    def get_publish_time(self,info):
        try:
            final_time = []
            str_time = info.body.find_all("div",class_="content")
            for i in str_time:
                t = i.find_all("p",class_="from")
                t = t[-1]
                b=''
                for word in t.text:
                    if word != ' ' and word != '\n':
                        b += word
                publish_time = b.split('\xa0')[0]
                print(publish_time)
                if '刚刚' in publish_time:
                    publish_time = datetime.now().strftime('%Y-%m-%d%')
                elif '分钟' in publish_time:
                    minute = publish_time[:publish_time.find('分钟')]
                    minute = timedelta(minutes=int(minute))
                    publish_time = (datetime.now() - minute).strftime('%Y-%m-%d% H:%M')
                    publish_time = publish_time[0:10]
                elif '今天' in publish_time:
                    today = datetime.now().strftime('%Y-%m-%d')
                    publish_time = today 
                elif '月' in publish_time:
                    year = publish_tme[0:4]
                    month = publish_time[5:7]
                    day = publish_time[8:10]
                    publish_time = year + '-' + month + '-' + day 
                final_time.append(publish_time)
            return final_time
        except Exception as e:
            print('Error:',e)
