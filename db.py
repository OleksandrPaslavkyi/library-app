import pyodbc
from config import Config

def create_database():
    connection = pyodbc.connect(Config.AZURE_DATABASE_CONNECTION)
    cursor = connection.cursor()

    check_table_query = """
    IF NOT EXISTS (
        SELECT * FROM sysobjects 
        WHERE name='books' AND xtype='U'
    )
    CREATE TABLE books (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255) NOT NULL,
        author NVARCHAR(255),
        description NVARCHAR(MAX),
        year NVARCHAR(4),
        genre NVARCHAR(50)
    )
    """
    cursor.execute(check_table_query)
    connection.commit()
    cursor.close()
    connection.close()

create_database()
print("Database and tables created successfully.")
