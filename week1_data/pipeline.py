import pandas as pd
import sqlalchemy as sa
import sys
import os
import argparse

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    #dwnl the csv
    arch_name = 'output.gz'
    csv_name = 'output.csv'

    os.system(f'wget {url} -O {arch_name} && gzip -d -c {arch_name} > {csv_name} && rm {arch_name}')



    engine = sa.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #creating schema
    df_schema = pd.read_csv(csv_name, nrows=0, \
                    parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    df_schema.to_sql(con=engine, name=table_name, if_exists= 'replace')


    df_iter = pd.read_csv(csv_name, \
                    parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], \
                    iterator=True, chunksize=100000 )

    import tqdm
    for chunk in tqdm.tqdm(df_iter):
        chunk.to_sql(con=engine, name=table_name, if_exists='append')





print(sys.argv)

# day = sys.argv[1]




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres') 
    parser.add_argument('--port', help='port for postgres') 
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to') 
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)





print(f'job has finished successfully')
