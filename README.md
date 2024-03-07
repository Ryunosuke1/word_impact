[Japanese](https://github.com/Ryunosuke1/word_impact/blob/main/README_japanese.md)
# Word Impact(News Article and Stock Price Relationship Calculator)

This program is a tool for calculating the relationship between news articles and stock prices of companies. Based on the user-provided company symbol, start date, and number of days to retrieve, it analyzes the content of news articles and the fluctuation of stock prices to assign weights to relevant words.

## Features

- Retrieves the latest news articles for the user-provided company.
- Extracts words from the news article content and calculates the frequency of occurrence for each word.
- Computes the percentage change in stock price after the specified number of days from the publication date of each article.
- Combines the frequency of word occurrence with the percentage change in stock price to calculate the importance of each word.
- Calculates the value of an arbitrary text by summing the importance of words contained within it.

## Usage

1. Run the `main.py` file.
   ```
   python3 main.py
   ```
3. Enter the following information in the displayed GUI:
   - Company symbol
   - Start date (in YYYY-MM-DD format)
   - Number of days to retrieve
4. Click the "Calculate and Save" button to execute the calculation.
5. The result will be saved in the `results.txt` file.
6. Input any text and click the "Load and Calculate" button to determine its value.

## Dependencies

- Python 3.x
- requests
- beautifulsoup4
- sympy

These dependencies are included in the `requirements.txt` file. Before running the project, please install the dependencies using `requirements.txt`:

```
pip install -r requirements.txt
```
## Setting Up API Keys

This program utilizes the Financial Modeling Prep API and the News API. Please obtain your API keys and set them appropriately within the `main.py` file.

```python
api_key_fmp = "YOUR_FINANCIAL_MODELING_PREP_API_KEY"
api_key_news = "YOUR_NEWS_API_KEY"
```
By providing clear instructions on how to set up API keys, dependencies, and usage, this README will help users understand and utilize the project effectively.

---

This may be wrong.
You should check the source cord.
