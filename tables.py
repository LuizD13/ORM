from sqlalchemy import Table, MetaData, Column, BigInteger, String, DateTime, insert, ForeignKey, func

meta = MetaData('global')

perfis = Table('perfis',
               meta,
               Column('id_perfil',BigInteger,primary_key=True,autoincrement=True),
               Column('descricao',String(100),nullable=False),
               Column('created_at',DateTime,nullable=False,server_default=func.now()))

perfisInsert = insert(perfis).values([{'descricao':"ADMINISTRADOR"},
                                      {'descricao':'TESTE'}])

empresas = Table('empresas',
                 meta,
                 Column('id_empresa',BigInteger,primary_key=True,autoincrement=True),
                 Column('id_parent_empresa',BigInteger,server_default='-1'),
                 Column('razao_social',String(100),nullable=False),
                 Column('created_at',DateTime,nullable=False,server_default=func.now()),
                 Column('id_perfil',BigInteger,ForeignKey('perfis.id_perfil',ondelete='CASCADE'),nullable=False))

listTables = [perfis,empresas]
listInserts = [perfisInsert]