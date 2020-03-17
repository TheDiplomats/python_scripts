import phoenixdb
import phoenixdb.cursor


#keytab_path = 'C:\\Users\\s314856\\Documents\\devl\\workspaces\\PhoenixJdbcClient\\src\\main\\resources\\s314856.keytab'

#database_url = 'http://hdpnode03.aepsc.com,hdpnode02.aepsc.com,hdpnode01.aepsc.com:2181:/hbase-secure'
#database_url = 'http://hdpnode03.aepsc.com:2181'
#database_url = 'jdbc:phoenix:hdpnode03.aepsc.com,hdpnode02.aepsc.com,hdpnode01.aepsc.com:2181;authentication=SPNEGO;principal=s314856@HDPDEV.AEPSC.COM;keytab=C:\\Users\\s314856\\Documents\\devl\\workspaces\\PhoenixJdbcClient\\src\\main\\resources\\s314856.keytab'

database_url = 'http://hdpnode01.aepsc.com:2181'

conn = phoenixdb.connect(database_url, autocommit=True)

cursor = conn.cursor()
cursor.execute("SELECT * FROM SYSTEM.CATALOG")
print(cursor.fetchall())