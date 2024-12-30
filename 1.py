import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# 字体问题
plt.rcParams['font.family'] = 'SimHei'  # 指定字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.rcParams['font.size'] = 5
plt.rcParams['figure.dpi'] = 300

# 指定文件路径
excel_file_path = '软件22级综测总表 终.xlsx'
csv_file_path = '软件22级综测总表.csv'

# 使用pandas读取Excel文件、并处理为更高度结构化的数据写入csv
df = pd.read_excel(excel_file_path,skiprows=(0,2))
df=df.drop(columns=df.columns[-1])
df.columns = df.columns[:-3].tolist() + ['综合测评总分']+ ['综测排名']+ ['智育排名']
df.fillna(0)#异常（无）成绩记为0
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
df = df.set_index([df.columns[0], df.columns[1], df.columns[2]], drop=True)
subject_df=df.iloc[:,0:21]
after_calculate_df=df.iloc[:,21:]

df_s=pd.DataFrame({"学科":df.columns[0:21],
                  "最大值":subject_df.max(),
                  '最小值':subject_df.min(),
                  '平均值':subject_df.mean(),
                  '中位数':subject_df.median(),
                  '标准差':subject_df.std(),
                  '挂科人数':subject_df.apply(lambda x: (x < 60).sum())
                })
df_s.to_csv('课程分析.csv', index=False, encoding='utf-8-sig')
for i in df_s.columns[1:]:
    ax=sns.barplot(
        data=df_s,x=i,y='学科'
    )
    ax.bar_label(ax.containers[0], fontsize=10)
    plt.savefig(f'每个学科的{i}.jpg')
    plt.show()
    
df_g=pd.DataFrame({
    '姓名':df.index.get_level_values('姓名'),
    "智育总分":after_calculate_df['智育总分70%'],
    '综测总分':after_calculate_df['综合测评总分'],
    })
df_g.to_csv('综测分析.csv', index=False, encoding='utf-8-sig')

sns.relplot(df_g,x='智育总分',y='综测总分',hue='姓名', sizes=(10, 20))
plt.savefig('每个人的综测与智育分数.jpg')
plt.show()

sns.lmplot(df_g,x='智育总分',y='综测总分',scatter_kws={'s': 5})
plt.savefig('综测与智育的相关性.jpg')
plt.show()