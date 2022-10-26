import pandas as pd

git_path = '/Users/benjaminmoran/Documents/GitHub/RenText'
csv_file = 'tcp_ids_and_dates.csv'
file_path = f'{git_path}/{csv_file}'

read_csv = pd.read_csv(file_path)
books_df = pd.DataFrame(data=read_csv)
books_df.columns = ['TCP Number','Year']
books_df = books_df.reset_index()
count_df = pd.DataFrame(columns= ['Year', 'Number of TCP Books'])
count_df = count_df.reset_index()

# # print(books_df)

def count_by_year():

    for index,row in books_df.iterrows():
        print(row[0], row[1], row[2])


if __name__ == "__main__":
    count_by_year()




