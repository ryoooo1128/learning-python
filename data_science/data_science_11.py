import random


#機械学習

#データを学習用データとテスト用データに分ける
def split_data(data, prob):
	results = [], []
	for row in data:
		results[0 if random.random() < prob else 1].append(row)
	return results

#学習用データとテスト用データを紐付ける
def train_test_split(x, y, test_pct):
	data = zip(x, y)
	train, test = split_data(data, 1 - test_pct)
	x_train, y_train = zip(*train)
	x_test, y_test = zip(*test)
	return x_train, x_test, y_train, y_test

#学習とテスト例
model = SomeKindOfModel()
x_train, x_test, y_train, y_test = train_test_split(xs, ys, 0,33)#テストデータを1/3にする
model.train(x_train, y_train)
performance = model.test(x_test, y_test)




#正解率
def accuracy(tp, fp, fn, tn):
	correct = tp + tn
	total = tp + fp + tn + fn

	return correct / tatal

print(accuracy(70, 4930, 13930, 981070))#0,98114



#適合率：陽性と判断した中で正解率
def precision(tp, fp, fn, tn):
	return tp / (tp + fp)

print(precision(70, 4930, 13930, 981070))#0.014



#再現率：本当は正解の中で陽性と判断した確率
def recall(tp, fp, fn, tn):
	return tp / (tp + fn)

print(recall(70, 4930, 13930, 981070))#0.005


#どちらの値も値が低いのはモデルが良くないため
#F1・調和平均：適合率と再現率の間になる
def f1_score(tp, fp, fn, tn):
	p = precision(tp, fp, fn, tn)
	r = recall(tp, fp, fn, tn)

	return 2 * p * r / (p + r)

