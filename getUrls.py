import os
import sqlite3

history_path=r"C:\Users\linsi\AppData\Local\CentBrowser\User Data\Default\History"
already_path=r"D:\getUcdrsUrls\already_buy.txt"
today_path=r"D:\AllDowns\today_buy.txt"

def get_urls():
# 数据库操作，得到历史数据中所有的网址
    c=sqlite3.connect(history_path)
    cursor=c.cursor()
    pattern_str='http://book.ucdrs.superlib.net/views/specific/%'
    # 只取出5天之内的，这样规模会小一些...
    select_statement="SELECT urls.url FROM urls,visits WHERE date(last_visit_time/1000000-11644473600,'unixepoch','localtime')>date('now','-1 days') AND urls.id=visits.url AND urls.url LIKE '{}' ORDER BY last_visit_time".format(pattern_str)
    # select_statement="SELECT urls.url FROM urls,visits WHERE urls.id=visits.url AND urls.url LIKE '{}' AND datetime('now','-1 day','last_visit_time')>1".format(pattern_str)
    print(select_statement)
    cursor.execute(select_statement)
    results=cursor.fetchall()
    urls=[]
    for each in results:
        url=each[0]
        if not url in urls:
            urls.append(url)

    with open(already_path,"r",encoding="utf-8") as f:
        already_urls=f.readlines()

    new_urls=[]
    for url in urls:
        if not url+"\n" in already_urls:
            print(url)
            new_urls.append(url)

    new_urls_s="\n".join(new_urls)

    with open(already_path,"a",encoding="utf-8") as f:
        f.write(new_urls_s)
        f.write("\n")

    with open(today_path,"w",encoding="utf-8") as f:
        f.write(new_urls_s)
        f.write("\n")

    print("done.")

    # print(url)

def main():
    get_urls()

if __name__ == '__main__':
    main()