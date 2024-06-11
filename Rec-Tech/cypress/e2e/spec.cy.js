describe('Conjunto de Testes Iniciais', () => {
  before(() => {
    // Renomeia o banco de dados existente, se houver
    cy.exec('if [ -f db.sqlite3 ]; then mv db.sqlite3 db_backup.sqlite3; fi', { failOnNonZeroExit: false });
    cy.exec('rm db.sqlite3', { failOnNonZeroExit: false }); // Remove o banco de dados existente
    cy.exec('python3 manage.py makemigrations', { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec('python3 manage.py migrate', { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec('python3 manage.py tests', { failOnNonZeroExit: false });
    // Inicie o servidor em modo de execução contínua. Isso precisa ser feito fora do Cypress, geralmente em um terminal separado.
  });

  it('Caso de teste para garantir que o ambiente está configurado corretamente', () => {
    // Verifica se o comando anterior foi bem-sucedido e se o teste pode ser executado
    expect(true).to.be.true;
  });
});

describe('Conjunto de testes para Admins', () => {
  let randomEmail;
  let randomName;
  let randomAddress;

  before(() => {
    randomEmail = `user_${Math.random().toString(36).substring(2, 11)}@test.com`;
    randomName = `Name_${Math.random().toString(36).substring(2, 11)}`;
    randomAddress = `Av 17 de agosto ${Math.floor(Math.random() * 1000) + 1}`;

    cy.visit('http://127.0.0.1:8000/auth/login/'); 
    cy.get('.login-link').click();
    cy.get('[type="text"]').type(randomName);
    cy.get('[type="email"]').type(randomEmail);
    cy.get('[type="password"]').type('123');
    cy.get('#user-type').select('admin');
    cy.get('.cadastro-button').click();
  });

  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/auth/login/'); 
    cy.get('[placeholder="Usuário"]').type(randomName);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();
    cy.visit('http://127.0.0.1:8000/admin_app/home/');
  });

  it('Caso de teste Lixeiras Cadastradas', () => {
    cy.get('#tipo_residuo').select('reciclaveis');
    cy.get('#botao-filtro').click();
  });

  it('Caso de teste Cadastrar Lixeira', () => {
    cy.get('#cadastrar_lixeira').click();
    cy.get('#domicilio').select('condominio');
    cy.get('#localizacao').type(randomAddress);
    //cy.get('#bairro').select(); // falta adicionar bairros
    //cy.get('#cliente-lixeira').select(randomName); // falta adicionar cliente
    cy.get('#tipo_residuo').select('reciclaveis');
    cy.get('#capacidade_maxima').type('100');
    cy.get('#estado_atual').type('50');
    cy.get('button').click();
  });

  it('Caso de teste de Avisos', () => {
    cy.get('#aviso_lixeira').click();
  });

  it('Caso de teste de Lixo por Bairro', () => {
    cy.get('#vialuzar_bairro').click();
  });

  it('Caso de teste Avaliar Coletas', () => {
    cy.get('#avaliar_coleta').click();
    cy.get('#sair').click();
  });
});

describe('Conjunto de testes para Clientes', () => {
  let randomEmail;
  let randomName;
  let randomAddress;

  beforeEach(() => {
    randomEmail = `user_${Math.random().toString(36).substring(2, 11)}@test.com`;
    randomName = `Name_${Math.random().toString(36).substring(2, 11)}`;
    randomAddress = `Av 17 de agosto ${Math.floor(Math.random() * 1000) + 1}`;

    cy.visit('http://127.0.0.1:8000/auth/login/');
    cy.get('.login-link').click();
    cy.get('[type="text"]').type(randomName);
    cy.get('[type="email"]').type(randomEmail);
    cy.get('[type="password"]').type('123');
    cy.get('#user-type').select('cliente');
    cy.get('.cadastro-button').click();

    cy.get('[placeholder="Usuário"]').type(randomName);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();
    cy.visit('http://127.0.0.1:8000/cliente_app/home/');
  });

  it('Caso de teste Perfil', () => {
  });

  it('Caso de teste Manutenção', () => {
    cy.get('#filtro_lixeira').click();
    cy.get('#data_manutencao').type('2024-07-23');
    cy.get('#tempo_manutencao').type('12:00');
    //cy.get('.custom-select').select(); // sem lixeiras para selecionar
    cy.get('#motivo_manutencao').type('está cheia');
    cy.get('.custom-button').click();
  });

  it('Caso teste de Avaliar Coleta', () => {
    cy.get('#avaliar_coleta').click();
    cy.get('#sair').click();
  });
});

describe('Conjunto de testes para Coletores', () => {
  let randomEmail;
  let randomName;
  let randomAddress;

  beforeEach(() => {
    randomEmail = `user_${Math.random().toString(36).substring(2, 11)}@test.com`;
    randomName = `Name_${Math.random().toString(36).substring(2, 11)}`;
    randomAddress = `Av 17 de agosto ${Math.floor(Math.random() * 1000) + 1}`;

    cy.visit('http://127.0.0.1:8000/auth/login/');
    cy.get('.login-link').click();
    cy.get('[type="text"]').type(randomName);
    cy.get('[type="email"]').type(randomEmail);
    cy.get('[type="password"]').type('123');
    cy.get('#user-type').select('coletor');
    cy.get('.cadastro-button').click();

    cy.get('[placeholder="Usuário"]').type(randomName);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();
    cy.visit('http://127.0.0.1:8000/coletor_app/home/');
  });

  it('Caso de teste Perfil', () => {
    
  });
  it('Caso teste de Rotas de Coleta', () => {
    cy.get('#vizualizar_lixeira').click();
    cy.get('#tipo_residuo').select('reciclaveis');
    cy.get('#domicilio').select('condominio');
    cy.get('[method="get"] > button').click();
    cy.get('#localizacao_atual').type(randomAddress);
    cy.get('.mt-3 > button').click();
    cy.get('#sair').click();
  });
});
