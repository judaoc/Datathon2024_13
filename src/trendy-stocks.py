from yahoo_fin import stock_info as si
import pandas as pd

def get_trendy():
    try:
        trending_stocks = si.get_day_most_active()
        trending_df = pd.DataFrame(trending_stocks)
        return(trending_df.head(3))

    except Exception as e:
        return(f"An error occurred: {e}")
