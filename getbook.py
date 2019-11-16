import requests
from bs4 import BeautifulSoup
import bs4
  
def getHTMLText(url,code='UTF-8'):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return ''
  
def fillUnivList(ulist,html):  #爬取列表及链接
    soup=BeautifulSoup(html,'html.parser') 
    for dd in soup.find_all('dt')[1].next_siblings:
        try:
            if isinstance(dd,bs4.element.Tag):
                #print(dd.a.string)
                Chapter_Name=dd.a.string
                Chapter_Link=(dd.a.attrs['href'][12:])
                ulist.append([Chapter_Name,Chapter_Link])
        except:
            continue
  
def getBookContent(uinfo,fpath,page_url):   #爬取章节内容
    count=0
    for i in range(len(uinfo)):
        url=page_url+uinfo[i][1]
        html=getHTMLText(url)
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write( uinfo[i][0] + '\n' )
        soup=BeautifulSoup(html,'html.parser')
        Tag=soup.find('div',id='content')
        try:
            for br in Tag:
                if isinstance(br,bs4.element.NavigableString):
                    with open(fpath, 'a', encoding='utf-8') as f:
                        f.write( str(br) + '\n' )
                    count = count + 1
                    print('\r                                                              ',end='')  #刷新进度
                    print('\r正在保存 {0:^20},总进度：{1:.2f}%'.format(uinfo[i][0],count/len(uinfo),chr(12288)),end='')  #显示进度
        except:
            continue
  
def main():  #主函数
    chapter_name_link=[]         #保存章节名和链接的列表
    page_url='https://www.qu.la/book/85467/'
    html=getHTMLText(page_url)
    output_file = 'C:/重生之都市仙尊.txt'
    fillUnivList(chapter_name_link,html)
    getBookContent(chapter_name_link,output_file,page_url)
  
  
main()