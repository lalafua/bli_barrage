import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


with open('cid.txt', mode='r', encoding='utf-8') as file:
     cids = file.readlines()

for cid in cids:
    cid = eval(cid)
    # 读取CSV文件
    df = pd.read_csv(f"{cid}\{cid}.csv".format(cid), encoding='utf-8', delimiter=',')

    # 去除无意义词
    stopwords_file = r"hit_stopwords.txt"
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    
    df['弹幕内容'] = df['弹幕内容'].apply(lambda x: ' '.join([word for word in jieba.cut(x) if word not in  stopwords]))

    # 统计词频并生成词云图
    danmustr = ' '.join(df['弹幕内容'])

    words = ' '.join(df['弹幕内容'])
    word_counts = Counter(words.split())
    top_words = dict(word_counts.most_common(100))
   
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='STSONG.TTF').generate_from_frequencies(top_words)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'{cid}\{cid}(词云图).png'.format(cid))

    import matplotlib.dates as mdates
    
    # 将弹幕时间列转换为日期时间类型
    df['弹幕时间'] = pd.to_datetime(df['弹幕时间'])
    # 设置时间范围
    start_date = pd.to_datetime('2023-03-15')
    end_date = pd.to_datetime('2023-05-25')
    # 过滤在时间范围内的数据
    filtered_df = df[(df['弹幕时间'] >= start_date) & (df['弹幕时间'] <= end_date)]
    # 按日期统计弹幕数量
    daily_counts = filtered_df['弹幕时间'].dt.date.value_counts().sort_index()
    # 创建柱状图
    fig, ax = plt.subplots(figsize=(12, 8))
    # 设置柱状图的宽度
    bar_width = 0.6
    # 生成颜色列表
    colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightskyblue']
    
    # 绘制每根柱子
    for i, (date, count) in enumerate(daily_counts.items()):
        # 确定每根柱子的位置
        x = mdates.date2num(date)
        # 设置每根柱子的颜色
        color = colors[i % len(colors)]
        # 绘制柱状图
        ax.bar(x, count, width=bar_width, color=color)
        # 在柱子上方标明具体日期
        for x, count, date in zip(daily_counts.index, daily_counts.values, daily_counts.index):
            ax.text(x, count, str(date.day), ha='center', va='bottom')

    # 设置 x 轴日期的格式
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=90)
    
    # 设置 x 轴刻度的间隔为一天
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xlabel('日期')
    plt.ylabel('弹幕量')
    plt.title('每天弹幕量统计')
    plt.tight_layout()
    plt.savefig(f'{cid}\{cid}(每日弹幕量统计_柱状图).png'.format(cid))

