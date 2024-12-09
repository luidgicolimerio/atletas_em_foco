# Trecho Padrão para criar banco de dados com SQLAlchemy
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base

"""
Usuario
<<id>> ID_Usuário: int
Nome [1]: str
Email [1]: str
Senha: str 
Data_Cadastro: date

Carteira
ID_Carteira: int
Saldo Tokens: float

Notícia
ID_Notícia (chave primária): int
Título: str 
Conteúdo: str 
Data_Publicação: date

Premiação
ID_Troca: int
ID_Usuário: int
ID_Premiação: int
Data_Troca: int
Tokens_Gastos: float
Nome prêmio: str
Descrição prêmio: str
"""

engine = create_engine('sqlite:///atividades.db')
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

#Tabelas

class Users(Base):
    __tablename__ = 'users' # Nome da tabela

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), index=True)
    email = Column(String(40), index=True)
    senha = Column(String(8), index=True)
    data_de_cadastro = Column(Date, default=date.today)

    def __repr__(self):
        return f'<User {self.nome}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def exclui(self): # TO-DO DELETE CASCADE
        db_session.delete(self) 
        db_session.commit()

class Carteira(Base):
    __tablename__ = 'carteira' # Nome da tabela
    id = Column(Integer, primary_key=True)
    saldo = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id')) 
    user = relationship("Users") # Usuário possui carteira

    def __repr__(self): # Representação do Objeto
        return f'<Saldo {self.saldo}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()

class Noticia(Base):
    __tablename__ = 'noticia' # Nome da tabela
    id = Column(Integer, primary_key=True)
    categoria = Column(Integer, ForeignKey('categoria.id')) 
    titulo = Column(String(40), index=True)
    conteudo = Column(String(1000), index=True)

    def __repr__(self):
        return f'<Noticia {self.titulo}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def exclui(self):
        db_session.delete(self)
        db_session.commit()

class Categoria(Base):
    __tablename__ = 'categoria' # Nome da tabela
    id = Column(Integer, primary_key=True)
    esporte = Column(String(40), index=True)

    def __repr__(self):
        return f'<Categoria {self.esporte}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def exclui(self):
        db_session.delete(self)
        db_session.commit()

    
class Premiacao(Base):
    __tablename__ = 'premiacao' # Nome da tabela
    id_premicao = Column(Integer, primary_key=True)
    valor = Column(Integer)
    nome = Column(String(40), index=True)
    descricao = Column(String(500), index=True)

    def __repr__(self):
        return f'<Premiacao {self.nome}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def exclui(self):
        db_session.delete(self)
        db_session.commit()

class Troca(Base):
    __tablename__ = 'troca' # Nome da tabela
    id_troca = Column(Integer, primary_key=True)
    premio_id = Column(Integer, ForeignKey('premiacao.id_premicao')) 
    # premio = relationship("Premiacao")
    user_id = Column(Integer, ForeignKey('users.id')) 
    # user = relationship("Users") 

    def __repr__(self):
        return f'<Troca {self.id_troca}>'
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    

# Função para criar o banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()