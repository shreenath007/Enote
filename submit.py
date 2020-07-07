from argparse import ArgumentParser
import pyodbc 
import pandas as pd
import argparse

def main():
    def get_data(filename):
        df = pd.read_csv(filename,low_memory=False)
        return df.dropna(how='all')
    
    df_person = get_data("BI_assignment_person.csv")
    df_person = df_person.fillna(value=0)
    df_account = get_data("BI_assignment_account.csv")
    df_transaction = get_data("BI_assignment_transaction.csv")
    
    df_transaction['transaction_date']= pd.DatetimeIndex(df_transaction['transaction_date'])
    df_transaction['transaction_month'] = df_transaction['transaction_date'].apply(lambda x: '{:02d}'.format(x.month)+'.'+'{:04d}'.format(x.year))
    server = 'DESKTOP-9C8N45J\SHREENATHSQL'
    database = 'Customers_Detail'
    #driver = '{SQL Server}'
    username = 'sa'
    password = 'shree12345'
    conn_sec = 'yes'
    # define our connection string 
    cnxn = pyodbc.connect('DRIVER={SQL Server}', \
                           SERVER = server, \
                           DATABASE=database, \
                           UID=username,\
                           PWD=password, \
                           Trusted_Connection=conn_sec)

    cursor = cnxn.cursor()
    for index,row in df_person.iterrows():
        try:
            cursor.execute("INSERT INTO dbo.person([id_person],[name],[surname],[zip],[city],[country],[email],[phone_number],[birth_date]) values (?,?,?,?,?,?,?,?,?)",row['id_person'],row['name'],row['surname'],row['zip'],row['city'],row['country'],row['email'],row['phone_number'],row['birth_date']) 
            cnxn.commit()
        except Exception as ex:
            print(ex)
            pass
        
    query_select_account = 'SELECT * FROM Customers_Detail.[dbo].[account]'
    account_data = pd.read_sql_query(query_select_account, cnxn)

    for index,row in df_account.iterrows():
        try:
            cursor.execute("INSERT INTO dbo.account([id_account],[id_person],[account_type]) values (?,?,?)",row['id_account'],row['id_person'],row['account_type']) 
            cnxn.commit()
        except Exception as ex:
            print(ex)
            pass

    query_select_transaction = 'SELECT * FROM Customers_Detail.[dbo].[transaction_2]'
    transaction_data = pd.read_sql_query(query_select_transaction, cnxn)
    transaction_data

    for index,row in df_transaction.iterrows():
        try:
            cursor.execute("INSERT INTO dbo.transaction_2([id_transaction],[id_account],[type],[date],[amount],[month]) values (?,?,?,?,?,?)",row['id_transaction'],row['id_account'],row['transaction_type'],row['transaction_date'],row['transaction_amount'],row['transaction_month'])
            cnxn.commit()
        except Exception as ex:
            print(ex)
            pass

    query_person = 'SELECT * FROM Customers_Detail.[dbo].[person]'
    query_account = 'SELECT * FROM Customers_Detail.[dbo].[account]'
    query_transaction = 'SELECT * FROM Customers_Detail.[dbo].[transaction_2]'
    df_person = pd.read_sql_query(query_person, cnxn)
    df_account = pd.read_sql_query(query_account, cnxn)
    df_transaction = pd.read_sql_query(query_transaction, cnxn)
    
    target_id = [1234,345]
    target_person_df = df_person[df_person['id_person'].isin(target_id)]
    target_account_df = df_account[df_account['id_person'].isin(target_id)]
    target_account_df.reset_index(drop=True, inplace=True)
    
    target_account = target_account_df['id_account'].values.tolist()
    target_transaction_df = df_transaction[df_transaction['id_account'].isin(target_account)]
    target_transaction_df.drop(columns=['id_transaction', 'date', 'type'], inplace=True)
    target_transaction_df.reset_index(drop=True, inplace=True)
    target_transaction_df = target_account_df.merge(target_transaction_df)[['id_account','amount','month','id_person']]
    result_df = target_transaction_df.groupby(['id_person','month'])['amount'].sum().reset_index()
    result_df.columns = ['id_person', 'month','sum_of_transactions']
    result_df = result_df.sort_values(by='id_person', ascending=False)
    print("\n### Final Report by using python pandas ###\n")
    result_df = result_df.reset_index(drop=True)
    print('result_df')
    print(result_df)
    cursor = cnxn.cursor()
    query_result = "SELECT account.id_person,transaction_2.month,SUM(transaction_2.amount) FROM account,transaction_2 WHERE (account.id_person=1234 OR account.id_person=345) AND account.id_account=transaction_2.id_account GROUP BY account.id_person,transaction_2.month ORDER BY account.id_person DESC;"
    result = pd.read_sql_query(query_result, cnxn)
    result.columns = ['id_person', 'month','sum_of_transactions']
    cursor.close()
    cnxn.close()
    print("\n### Final Report by using sql query ###\n")
    print(result)
    
if __name__ == "__main__":
    main()




