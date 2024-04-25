from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions={'cadastrar lixeiras': True, 'vizualizar lixeiras':True}

class Cliente(AbstractUserRole):
    available_permissions={'solicitar manutenção': True}
class Coletor(AbstractUserRole):
    available_permissions={'vizualizar rotas':True}