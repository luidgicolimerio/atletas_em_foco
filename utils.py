from models import Users, Carteira, Categoria

def cria_conta(name, email, senha):
    user = Users(nome=name, email=email, senha=senha)
    user.save()
    carteira = Carteira(saldo=0, user=user)
    carteira.save()

def consulta_usuarios(i):
    user = Users.query.filter_by(id=i).first()
    print(user)
    carteira = Carteira.query.filter_by(user=user).first()
    print(carteira)

def soma_saldo(i, tokens):
    user = Users.query.filter_by(id=i).first()
    carteira = Carteira.query.filter_by(user=user).first()
    carteira.saldo += tokens
    carteira.save()
    print(carteira)

def subtrai_saldo(i, tokens):
    user = Users.query.filter_by(id=i).first()
    carteira = Carteira.query.filter_by(user=user).first()
    carteira.saldo -= tokens
    carteira.save()
    print(carteira)

def add_categoria(nome):
    categoria = Categoria(esporte=nome)
    categoria.save()

if __name__ == '__main__':
    # cria_conta('Luidgi','teste@gmail.com', 'teste123')
    # consulta_usuarios(1)
    # soma_saldo(1, 20)
    # consulta_usuarios(1)
    # subtrai_saldo(1)
    # add_categoria("futebol")
    # add_categoria("volei")
    # add_categoria("handball")
    # add_categoria("basquete")
    # add_categoria("mma")
    # add_categoria("rugby")
    ...