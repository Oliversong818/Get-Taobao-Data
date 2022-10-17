import pandas as pd
import numpy as np
import re #用正则表达式re.sub指令替换图片链接中的无效字符或者其他内容

pd.set_option('display.max_columns',None)  #显示全部列的内容
pd.set_option('display.unicode.ambiguous_as_wide', True) #标题和内容对齐的指令
pd.set_option('display.unicode.east_asian_width', True)
new_file = pd.read_excel('./男式眼镜.xlsx')
# new_file.rename(columns={'商品价格':'PRICE'},inplace=True)
# 数据清理的4个关键：数据一致性，空值（完整性），合理性，唯一型。尽量不要轻易删除有空值或者不合理值的行，会造成数据量不够。
new_file.dropna(how='all')  #把全部内容都为空的行去除
new_file['卖家位置'] = new_file['卖家位置'].fillna('其他') #把空的卖家位置用其他来填充
df = pd.DataFrame()
df[['fuhao','price']] = new_file['商品价格'].str.split('¥',expand=True)  #把商品价格中的符号和金额用¥拆分
df['price'] = df['price'].astype('float')  #把价格栏变成小数形式

new_file = pd.concat([new_file,df],axis=1)   #把拆分出来的金额和原表重新连接起来
new_file.drop('商品价格',axis=1,inplace=True)     #把旧的商品价格整列去除
df1 = pd.concat([new_file,df['price']],axis=1)

df2 = pd.DataFrame()
df2 =new_file['商品成交量'].str.split('人',expand=True)
df2.columns = ['人数','fukuan']
# df2.drop('fukuan',axis=1,inplace= True)
new_file = pd.concat([new_file,df2['人数']],axis=1)

new_file['人数'].replace(['100+','200+','1000+'],[100,200,1000],inplace=True) #把付款人数中的+替换掉，才能把这列变成整数类型
new_file.drop(['商品成交量','fuhao'],axis=1,inplace=True)
#
# df2['顾客人数']=df2['顾客人数'].replace('+','',inplace=True)
new_file['人数']=new_file['人数'].astype('int')  #把拆分出来的人数列变成整数型

new_file.columns = ['序号','商品图片','商品名称','卖家位置','商品价格','付款人数']  #重新命名列名
new_file.sort_values(['付款人数','商品价格'],ascending=[False,True],inplace=True)  #付款人数按降序，商品价格按升序进行排列

for i in range(0,440):  #在所有440行数据中把图片的链接遍历出来
    a = re.sub('_.webp','',new_file['商品图片'][i])  #用正则的SUB指令把遍历出来的多余字符_.webp用空值代替
    new_file['商品图片'][i] = a  #再次把商品图片中对应的链接替换为新的值a
new_file.to_excel('./男式眼镜11.xlsx',index=False)  #重新保存到文件中






