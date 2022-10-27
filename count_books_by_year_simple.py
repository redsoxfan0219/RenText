import pandas as pd
import re
import numpy as np


def __initialize_databases__(file_path):

    read_csv = pd.read_csv(file_path)
    books_df = pd.DataFrame(data=read_csv)
    books_df.columns = ['TCP_Number','Year']
    books_df = books_df.reset_index()
    count_df = pd.DataFrame(columns= ['Year', 'Number_of_TCP_Books'])
    count_df = count_df.reset_index()

    return books_df, count_df

def __clean_dataframe__(dataframe):

    books_df = dataframe

    # Remove questions marks altogether

    books_df['Year'] = books_df['Year'].map(lambda x: x.rstrip('?'))

    # 823/60325 rows contain a year range (1.36% of total). Format YYYY-YYYY.
    # Remove the terminus ad quo. Easiest way to do this is filter to those 
    # rows that include a '-' and eliminate the first 5 characters in the string.

    hyphen_mask = books_df['Year'].str.contains('-')

    years_with_hyphens = books_df[hyphen_mask]

    years_with_hyphens['cleaned_year'] = years_with_hyphens['Year'].map(lambda x: re.sub(r'.', '', x, count = 5))

    # Create cleaned_years as a new column within the original dataframe

    combined = books_df.join(years_with_hyphens['cleaned_year'])

    # Where no cleaning was needed, map the original year onto the clean_year column

    final_col = combined['cleaned_year'] = combined['cleaned_year'].combine_first(combined['Year'])
    books_df['cleaned_year'] = final_col
    cleaned_books_df = books_df

    # Ran the line to print a static file that I can use for later.

    # cleaned_books_df.to_csv('cleaned_tcp_nav.csv', index=False)

    return cleaned_books_df


def count_by_year():

    git_path = '/Users/benjaminmoran/Documents/GitHub/RenText'
    csv_file = 'tcp_ids_and_dates.csv'
    file_path = f'{git_path}/{csv_file}'
    books_df, count_df = __initialize_databases__(file_path)
    cleaned_books_df = __clean_dataframe__(books_df)

    # for index,row in books_df.iterrows():
    #     print(row[0], row[1], row[2])

    # cleaned_books_df = books_df.f


if __name__ == "__main__":
    count_by_year()




