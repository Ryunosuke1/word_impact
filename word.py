import requests
from bs4 import BeautifulSoup
import re
from sympy import symbols, Eq, solve
from decimal import Decimal, getcontext
from datetime import datetime, timedelta
import tkinter as tk
from threading import Thread


def extract_words(article):
    words = re.findall(r'\b\w+\b', article)
    return words

def get_company_name(symbol):
    api_key = ""  # Financial Modeling Prep APIのAPIキーを指定
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['companyName']
        else:
            print("Error: Company name not found for symbol", symbol)
            return None
    else:
        print("Error fetching company name:", response.status_code)
        return None

def get_news_articles(company_name):
    api_key = ""  # News APIのAPIキーを指定
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles_data = response.json()
        articles = [(article['publishedAt'], article['title']) for article in articles_data.get("articles", [])]
        return articles
    else:
        print("Error fetching articles:", response.status_code)
        return []

def get_stock_price_at_date(symbol, date):
    api_key = ""  # Financial Modeling Prep APIのAPIキーを指定
    date_str = date.strftime("%Y-%m-%d")
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'historical' in data:
        prices = data['historical']
        for entry in prices:
            if entry['date'] == date_str:
                return entry['close']
        
        for entry in prices:
            if entry['date'] < date_str:
                return entry['close']
        
        print("Error: Stock price information not found.")
        return None
    else:
        print("Error: Stock price information not found.")
        return None

def calculate_word_values(articles, symbol, start_date, delta_days):
    word_values = {}

    for pub_date, article in articles:
        words = article.split()
        for word in words:
            if word in word_values:
                word_values[word] += 1
            else:
                word_values[word] = 1

        start_datetime = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
        end_datetime = start_datetime + timedelta(days=delta_days)
        start_price = get_stock_price_at_date(symbol, start_datetime)
        end_price = get_stock_price_at_date(symbol, end_datetime)

        if start_price is not None and end_price is not None:
            price_change = (end_price - start_price) / start_price

            for word, count in word_values.items():
                word_values[word] = count * price_change

        else:
            print(f"Error fetching stock price information for article published on {pub_date}")

    return word_values

def calculate_button_click():
    query = text_input.get("1.0", tk.END).strip()
    company_name = get_company_name(query)
    articles = get_news_articles(query)
    start_date = text_date.get("1.0", tk.END).strip()
    delta_days = int(text_delta_days.get("1.0", tk.END).strip())

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "計算中...\n")

    # 結果をファイルに書き出し
    word_values = calculate_word_values(articles, query, start_date, delta_days)
    with open("results.txt", "w") as file:
        for word, value in word_values.items():
            file.write(f"{word}: {value}\n")

    result_text.insert(tk.END, "計算結果を results.txt に保存しました。\n")

def read_and_calculate_button_click():
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "結果を読み込んで計算中...\n")

    # ファイルから結果を読み込み
    word_values = {}
    with open("results.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            word, value = line.strip().split(": ")
            word_values[word] = float(value)

    # 任意の文章の値を計算
    query_text = text_query.get("1.0", tk.END).strip()
    words = extract_words(query_text)
    total_value = sum(word_values.get(word, 0) for word in words)

    result_text.insert(tk.END, f"文章の値: {total_value}\n")

# GUIの作成
root = tk.Tk()
root.title("ニュース記事の計算")

text_symbol = tk.Label(root, text="シンボルを入力してください:")
text_symbol.pack()

text_input = tk.Text(root, height=1, width=50)
text_input.pack()

label_date = tk.Label(root, text="開始日を入力してください（YYYY-MM-DD形式）:")
label_date.pack()

text_date = tk.Text(root, height=1, width=20)
text_date.pack()

label_days = tk.Label(root, text="取得日数を入力してください:")
label_days.pack()

text_delta_days = tk.Text(root, height=1, width=20)
text_delta_days.pack()

button_calculate = tk.Button(root, text="計算して保存", command=calculate_button_click)
button_calculate.pack()

text_query_label = tk.Label(root, text="任意の文章を入力してください:")
text_query_label.pack()

text_query = tk.Text(root, height=4, width=50)
text_query.pack()

button_read_and_calculate = tk.Button(root, text="結果を読み込んで計算", command=read_and_calculate_button_click)
button_read_and_calculate.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
