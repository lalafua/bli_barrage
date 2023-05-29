import pandas as pd
import matplotlib.pyplot as plt

with open('cid.txt', mode='r', encoding='utf-8') as file:
     cids = file.readlines()

for cid in cids:
    cid = eval(cid)
    # 读取CSV文件
    df = pd.read_csv(f"{cid}\{cid}.csv".format(cid), encoding='utf-8', delimiter=',')
    # 将弹幕时间列转换为日期时间类型
    df['弹幕时间'] = pd.to_datetime(df['弹幕时间'])
    # 按时间段分类
    df['时间段'] = pd.cut(df['弹幕时间'].dt.hour, bins=[0, 6, 12, 14, 18, 24], labels=['wee hours', 'morning', 'noon', 'afternoon', 'night'], include_lowest=True)
    # 统计时间段内的弹幕数量
    time_counts = df['时间段'].value_counts()

    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 创建柱状图
    plt.figure(figsize=(8, 6))
    plt.bar(time_counts.index, time_counts.values)
    plt.xlabel('时期')
    plt.ylabel('弹幕数量')
    plt.title('不同时间段的弹幕数（柱状图）')
    plt.tight_layout()
    plt.savefig(f'{cid}\{cid}(不同时间段的弹幕数_柱状图).png'.format(cid))

    # 创建饼状图
    plt.figure(figsize=(8, 6))
    plt.pie(time_counts.values, labels=time_counts.index, autopct='%1.1f%%')
    plt.title('不同时间段的弹幕数（饼状图）')
    plt.axis('equal')
    plt.savefig(f'{cid}\{cid}(不同时间段的弹幕数_饼状图).png'.format(cid))
