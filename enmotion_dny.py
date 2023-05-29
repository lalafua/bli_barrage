import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt

with open('cid.txt', mode='r', encoding='utf-8') as file:
     cids = file.readlines()

for cid in cids:
    cid = eval(cid)
    # 读取CSV文件
    df = pd.read_csv(f"{cid}\{cid}.csv".format(cid), encoding='utf-8', delimiter=',')
    danmu_texts = df['弹幕内容']

    # 使用snownlp分析情感倾向并计算积极、消极和中立弹幕数量
    sentiments = [SnowNLP(text).sentiments for text in danmu_texts]

    positive_count = sum(1 for sentiment in sentiments if sentiment > 0.6)
    negative_count = sum(1 for sentiment in sentiments if sentiment < 0.4)
    neutral_count = len(sentiments) - positive_count - negative_count

    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 创建饼状图
    labels = ['积极', '消极', '中立']
    values = [positive_count, negative_count, neutral_count]

    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('弹幕情绪分析')
    plt.axis('equal')
    plt.savefig(f'{cid}\{cid}(情绪分析).png'.format(cid))
