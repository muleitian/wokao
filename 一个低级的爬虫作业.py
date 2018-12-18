# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 09:30:32 2018

@author: 何洪涛
"""

from bs4 import BeautifulSoup as Be
import requests as req
import os

BaseUrl = "http://www.52duzhe.com/"

def Do_soup(url):
    try:
        r = req.get(url,headers={'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        soup = Be(html,'lxml')
        return soup
    except:
        print("获取"+url+"失败")


def Search_each_Per(tag):
    aut_set = set()
    a_list = []
    for i in range(2010,2018):#划定年限的范围
        for j in range(1,25)://划定期数
            if j<10:
                ExtraUrl = str(i)+'_0'+str(j)
            else:
                ExtraUrl = str(i)+'_'+str(j)
            if i in [2010,2011,2012]:
                if(i == 2012 and j>=14):
                    url = BaseUrl + ExtraUrl + r"/index.html"
                else:
                    url = BaseUrl + '1_' + ExtraUrl + ".html"
            else:
                url = BaseUrl + ExtraUrl + r"/index.html"
            soup = Do_soup(url)  #使用函数
            if soup == None:
                continue
            per_aut_list = soup.find_all('td',class_="author")
            if tag==1:
                for k in per_aut_list:
                    aut_set.add(k.string)
                print("{}年{}期作者已入库".format(i,j))
            else:
                for k in per_aut_list:
                    a_list.append(k.string)
    if tag==1:
        return list(aut_set)    #返回了一个去重后的作者列表
    else:
        return a_list          #返回了一个有重复元素的列表，用于计数
    
def main():
    author_list0 = Search_each_Per(1)   # 1代表一个控制标记,接收无重列表
    print("正在接收有重复数据列表,请等待...")
    a_list = Search_each_Per(0)         #接收有重复元素列表
    result = {}                         #放结果的字典
    for i in author_list0:
        result[str(i)] = 0     #初始化统计结果
        for j in a_list:
            if i==j:
                result[str(i)] += 1
    #下面对结果按发表次数做降序处理
    print("下面对结果按发表次数做降序处理...")
    att = []              #做一个容器
    for key,value in result.items():
        j={}
        j["author"]=key
        j["times"]=value
        att.append(j)
    att.sort(key = lambda x:x["times"],reverse = True)
    # 将结果写入text文本中
    print("将结果写入text文本中,请耐心等待...")
    path = os.getcwd()
    filename = path + "读者作者结果1.txt"
    new = open(filename,"w",errors='ignore')   #网络字节流中可能有不合法字符要忽略：illegal multibyte sequence
    for i in att:
        author = i["author"]
        times = i["times"]
        print(author)
        print(times)
        if author == None:                       #unsupported operand type(s) for +: 'NoneType' and 'str'
            new.write("None" +"\t" + str(times) + "\n")
        else:
            new.write(author +"\t" + str(times) + "\n")
    new.close()
    print("完成统计")
main()
