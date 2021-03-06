#データの取得
import sys, re, csv
import collections
def process(date, symbol, price):
        print(date, symbol, price)



#egrep.py

#sys.argv：コマンドラインの引数のリスト
#sys.argv[0]：プログラム名
#sys.argv[1]：コマンドライン上で指定した正規表現

#正規表現に合致した各行を出力
regex = sys.argv[0]

for line in sys.stdin:
	if re.search(regex, line):
		sys.stdout.write(line)

#読み込んだテキストの行数を数えて出力
count = 0
for line in sys.stdin:
	count += 1
print(count)

#頻出するものを表示
try:
	num_words = int(sys.argv[1])
except:
	print("usage: most_common_words.py num_words")
	sys.exit(1)#0以外のexitコードはエラーが発生したことを示す

count = collections.Counter(word.lower()					#単語を小文字にする
							for line in sys.stdin
							for word in line.strip().split()#単語は空白で仕切る
							if word)						#空文字はスキップする

for word, count in counter.most_common(num_words):
	sys.stdout.write(str(count))
	sys.stdout.write("\t")
	sys.stdout.write(word)
	sys.stdout.write("\n")






#ファイルの読み込み
#基礎編
file_for_reading = open('reading_file.txt', 'r')#rはread-onlyを意味する
file_for_writing = open('writing-file.txt', 'w')#wは書き込みを意味する　既存ファイルを壊す可能性がある
file_for_appending = open('appending-file.txt', 'a')#aは追記を意味する　ファイルの末尾に追加する
file_for_writing.close()#使い終わったらクローズを必ずする

#クローズを忘れないために、自動化する：with内でのみファイルがopenになっている
with open(filename, 'r') as f:
	data = function_that_gets_data_from(f)#この時点ですでにクローズされている


#ファイル全体を読み込む時はforで行の読み込みを繰り返す
starts_with_hash = 0

with open('input.txt', 'r') as f:
	for line in file:				#ファイル内の各行ごとに繰り返す
		if re.match("^#", line):	#正規表現を使って行頭の'#'の有無を調べる
			starts_with_hash += 1	#行頭が'#'の行数を数える


#メールアドレスのドメインのデータを取得
def get_domain(email_adress):
	return email_adress.lower().split("@")[-1]#"@"で分割して後ろも部分を返す

with open('email_adress.txt', 'r') as f:
	domain_counts = Counter(get_domain(line.strip())
							for line in f
							if '@' in line)






#csv：カンマやタブでファイルが区切られている場合に使う
#日本語が含まれる場合は、文字化け防止でopen('japan.csv', encoding='UTF-8')と文字コードを指定する
with open('__tab_delimited_stock_prices.txt', 'r') as f:
	reader = csv.reader(f, delimiter = '\t')
	for row in reader:
		data = row[0]
		symbol = row[1]
		closing_price =float(row[2])
		process(data, symbol, closing_price)


with open('__colon_delimited_stock_prices.txt', 'r') as f:
	reader = csv.DictReader(f, delimiter = ':')
	for row in reader:
		data = row["date"]
		symbol = row["symbol"]
		closing_price = float(row["closing_price"])
		process(data, symbol, closing_price)


today_prices = { 'AAPL' : 90.91, 'MSFT' : 41.68, 'FB' : 64.5 }

with open('__comma_delimited_stock_prices.txt', 'w') as f:
	writer = csv.writer(f, delimiter = ',')
	for stock, price in today_prices.items():
		writer.writerow([stock, price])

