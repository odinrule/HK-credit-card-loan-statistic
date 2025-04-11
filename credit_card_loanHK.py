import pandas as pd
import requests
import json
import matplotlib
import matplotlib.pyplot as plt

matplotlib.font_manager.fontManager.addfont(
    'TaipeiSansTCBeta-Regular.ttf')  # 令matplotlib模組可以顯示中文
matplotlib.rc('font', family='Taipei Sans TC Beta')


# 1. 目標 url ，在https://apidocs.hkma.gov.hk/chi/documentation/market-data-and-statistics/monthly-statistical-bulletin/banking/credit-card-lending-survey/之內
url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/banking/credit-card-lending-survey"

# 2. Header毋須在此網站輸入

# 3. 向目標發送請求(request)
response = requests.get(url)
print(response)  # 200代表請求成功

# 4. 讀取 response 並進行decode
# 使用loads把資料轉為dict
dict_data = json.loads(response.content)

print(dict_data)
print(f"dict_data是{type(dict_data)}")

dump_data = dict_data["result"]["records"]  # 存取dict裡的list
print(dump_data)
print(f"dump_data是{type(dump_data)}")

with open("creditCardloanHK.txt", "w") as my_file:  # 製作txt檔,用作排版json,
    # json模組的屬性dumps()將dump_data轉為str，json字符串
    write_data = json.dumps(dump_data)
    my_file.write(write_data)
print(f"write_data是{type(write_data)}")

df = pd.DataFrame(dump_data)  # 將dump_data由list檔案轉為pandas的df(dataframe)
col_name = ["日期", "期末數字帳戶總數(千個)", "期末數字拖欠帳款超過90日（百萬港元）", "期內數字撇帳額(百萬港元)", "期內數字轉期帳款（百萬港元）",
            "期內數字平均應收帳款總額(百萬港元)"]  # 期內平均數 (計算方法為 [期初數額 + 期末數額]/2)
pd.set_option('display.max_rows', None)  # 顯示所有行
df = df.set_axis(col_name, axis=1)
df

df2 = df.iloc[::-1]  # 將df反向切片放入df2,切片後的index會被反轉為由大到小
# 將df2的index重設為由0開始, https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe
df2 = df2.reset_index(drop=True)
pd.set_option('display.max_rows', 6)  # 顯示df2其中6行
df2

df3 = pd.DataFrame(df2, columns=["日期", "期末數字帳戶總數(千個)"])
df3
df3 = df3.set_index("日期")
df3.plot(kind="line")
plt.show()

df4 = pd.DataFrame(df2, columns=["日期", "期末數字拖欠帳款超過90日（百萬港元）"])
df4
df4 = df4.set_index("日期")
df4.plot(kind="line")
plt.show()

df5 = pd.DataFrame(df2, columns=["日期", "期內數字撇帳額(百萬港元)"])
df5
df5 = df5.set_index("日期")
df5.plot(kind="line")
plt.show()

df6 = pd.DataFrame(df2, columns=["日期", "期內數字轉期帳款（百萬港元）"])
df6
df6 = df6.set_index("日期")
df6.plot(kind="line")
plt.show()

# 期內平均數 (計算方法為 [期初數額 + 期末數額]/2)
df7 = pd.DataFrame(df2, columns=["日期", "期內數字平均應收帳款總額(百萬港元)"])
df7
df7 = df7.set_index("日期")
df7.plot(kind="line")
plt.show()
