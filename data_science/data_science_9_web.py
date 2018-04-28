import sys, re
from bs4 import BeautifulSoup
import requests


#事例1
url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationData&page=1"
soup = BeautifulSoup(requests.get(url).text, 'html5lib')

#thumbtextタグを検索する
tds = soup('td', 'thumbtext')
print(len(tds))#30

#Videoを取り除く　span内にある
def is_video(td):#videoであるものを数える
	pricelabels = td('span', 'pricelabel')
	return len(pricelabels) == 1 and pricelabels[0].text.strip().startswish("Video")
	#Video：pricelabelが、空白を取り除いてVideoで始まるもの１つしか持たない

#情報収集の準備
def book_info(td):#tdタグに書籍のデータが入っているため、取り出して辞書にする
	#題名を取り出す　<div class="thumbheader"><a>
	title = td.find("div", "thumbheader").a.text

	#AuthorNameを取り出す　<div class="AuthorName"> By が前置されている
	title = td.find("div", "thumbheader").a.text
	author_name = td.find('div', 'AuthorName').text
	authers = [x.strip() for x in re.sub("^By ", "", author_name).split(",")]#re.sub(正規表現 ^は最初が一致を意味, 置換する文字列, 置換される文字列)

	#ISBNを取り出す　<div class="thumbheader"><a herf="/product/~.do">
	isbn_link = td.find("div", "thumbheader").a.get("href")
	isbn = re.match("/product/(.*)\.do", isbn_link).group(1)
	#findは正規表現が指定できないためre.matchを使う
	#.は任意の文字　*はその繰り返し

	#日付を取り出す　<span class="directorydate">
	date = td.find("span", "directorydate").text.strip()#stripは取り除く

	return {
		"title" : title,
		"author" : authors,
		"isbn" : isbn,
		"date" : date
	}



from bs4 import BeautifulSoup
import requests
from time import sleep
base_url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationData&page="


books =[]
NUM_PAGES = 30

for page_num in range(1, NUM_PAGES + 1):
	print("souping page", page_num, ",", len(books), " found so far")
	url = base_url + str(page_num)
	soup = BeautifulSoup(requests.get(url).text, 'html5lib')

	for td in soup("td", "thumbheader"):
		if not is_video(td):
			books.append(book_info(td))

def get_year(book):#dateの値はNovember 2014のようになっている
	return int(book["date"].split()[1])

year_counts = collections.Counter(get_year(book) for book in books
								 if get_year(book) <= 2018)

import matplotlib.pyplot as plt
years = sorted(year_counts)
book_counts = [year_counts[year] for year in years]
plt.plot(years, book_counts)
plt.ylabel("# of data books")
plt.title("Data is Big")
plt.show()



#サイトの仕様が変わったため現在は利用できない

