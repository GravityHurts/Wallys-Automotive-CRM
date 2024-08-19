import sqlite3
import pandas as pd

def sqlite_to_excel(database_file, excel_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    with pd.ExcelWriter(excel_file) as writer:
        for table in tables:
            table_name = table[0]
            df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
            df.to_excel(writer, sheet_name=table_name, index=False)

    cursor.close()
    conn.close()

sqlite_to_excel('../data/mechanic_app.db', '../output.xlsx')
