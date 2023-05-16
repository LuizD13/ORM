from sqlalchemy import create_engine, URL
from sqlalchemy.schema import CreateSchema
import logging
from datetime import datetime as dt

from tables import listTables,listInserts
from schemas import listSchemas


urlConn = URL.create(
    drivername="postgresql+psycopg2",
    username='postgres',
    password='admin',
    host='127.0.0.1',
    database='onboard',
    port=5432
)

def setLog():
    formatLog = "[%(asctime)s] - %(name)s %(levelname)s %(message)s"
    dtFormatLog = "%d/%m/%Y %H:%M:%S"
    
    ormFileLog = logging.getLogger('sqlalchemy.engine')
    ormFileLog.setLevel(logging.INFO)
    logging.basicConfig(filename=f'log_{dt.today().strftime("%d_%m_%Y")}.txt',
                        filemode='a',
                        format=formatLog,
                        datefmt=dtFormatLog)
    
    ormConsoleLog = logging.StreamHandler()
    ormConsoleLog.setLevel(logging.INFO)
    ormFileLog.addHandler(ormConsoleLog)
    
    logFormatter = logging.Formatter(formatLog,
                                    dtFormatLog)
    
    ormConsoleLog.setFormatter(logFormatter)

try:
    
    setLog()
    
    eng = create_engine(urlConn)
    con = eng.connect()

    for schema in listSchemas:
        if not con.dialect.has_schema(con,schema):
            con.execute(CreateSchema(schema,True))
            con.commit()
     
    for table in listTables:
        if not con.dialect.has_table(con,table.name,table.metadata.schema):   
            table.create(eng)
        
    for inserts in listInserts:
        stmt = inserts
        compiled = stmt.compile(eng)
        con.execute(compiled)
        con.commit()
    
except:
    pass



