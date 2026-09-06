mysql_username = 'root'
mysql_password = 'XjQJSHcU5WFp33svKdLSxUKS' # Replace with your server connect information
mysql_host = '172.21.236.31' # Replace with your server connect information
mysql_port = '3306' # Replace with your server connect information
database_name = 'Chinook'
mysql_uri = f'mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{database_name}'
db = SQLDatabase.from_uri(mysql_uri)