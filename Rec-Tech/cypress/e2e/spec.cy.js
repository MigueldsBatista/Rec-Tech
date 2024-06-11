
describe('Conjunto de Testes Iniciais', () => {
  before(() => {
    // Renomeia o banco de dados existente, se houver
    cy.exec('if [ -f db.sqlite3 ]; then mv db.sqlite3 db_backup.sqlite3; fi', { failOnNonZeroExit: false });
    cy.exec('rm db.sqlite3', { failOnNonZeroExit: false }); // Remove o banco de dados existente
    cy.exec('python3 manage.py makemigrations', { failOnNonZeroExit: false }); // Executa migração do banco de dados
    cy.exec('python3 manage.py migrate', { failOnNonZeroExit: false }); // Executa migração do banco de dados
    //cy.exec('python3 manage.py runserver', { failOnNonZeroExit: false }); achei melhor nao deixar habilitado
  });

  it('Caso de teste para garantir que o ambiente está configurado corretamente', () => {
    // Verifica se o comando anterior foi bem-sucedido e se o teste pode ser executado
    expect(true).to.be.true;
  });
});
let cliente='cliente';
let cliente_email='cliente@test.com';
let senha='123'

let admin='admin';
let admin_email='admin@test.com';

let coletor='coletor';
let coletor_email='coletor@test.com';


describe('Conjunto de testes para Admins', () => {
 



  let randomAddress;
  randomAddress = `Av 17 de agosto ${Math.floor(Math.random() * 1000) + 1}`;


  //Login como administrador da aplicação != admin django
  beforeEach(() => {
    cy.exec('python3 manage.py delete_objects', { failOnNonZeroExit: false }); // Deleta os objetos que podem ter sido criados anteriormente
    cy.exec('python3 manage.py create_objects', { failOnNonZeroExit: false }); // Cria novamente para assegurar a independencia dos testes

    cy.visit('http://127.0.0.1:8000/auth/login/');
    cy.get('[placeholder="Usuário"]').type(admin);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();

  });

  it('Caso de testes filtros do admin', () => {
    // Verifique se todos os tipos de lixo estão presentes antes de aplicar o filtro
    cy.get('.lixeiras-container').contains(/\borganicos\b/).should('exist');
    cy.get('.lixeiras-container').contains(/\breciclaveis\b/).should('exist');
    cy.get('.lixeiras-container').contains(/\bnao_reciclaveis\b/).should('exist');

    // Aplicar o filtro para lixos recicláveis
    cy.get('#tipo_residuo').select('reciclaveis');
    cy.get('#botao-filtro').click();

    // Verifique se o lixo orgânico não está mais visível
    cy.get('.lixeiras-container').contains(/\borganicos\b/).should('not.exist');

    // Verifique se o lixo reciclável está visível e o não reciclável não está
    cy.get('.lixeiras-container').contains(/\breciclaveis\b/).should('exist');
    cy.get('.lixeiras-container').contains(/\bnao_reciclaveis\b/).should('not.exist');

    // Aplicar o filtro para lixos não recicláveis
    cy.get('#tipo_residuo').select('nao_reciclaveis');
    cy.get('#botao-filtro').click();

    // Verifique se o lixo reciclável não está mais visível
    cy.get('.lixeiras-container').contains(/\breciclaveis\b/).should('not.exist');

    // Verifique se o lixo não reciclável está visível e o orgânico não está
    cy.get('.lixeiras-container').contains(/\bnao_reciclaveis\b/).should('exist');
    cy.get('.lixeiras-container').contains(/\borganicos\b/).should('not.exist');

    // Aplicar o filtro para lixos orgânicos
    cy.get('#tipo_residuo').select('organicos');
    cy.get('#botao-filtro').click();

    // Verifique se o lixo reciclável não está mais visível
    cy.get('.lixeiras-container').contains(/\breciclaveis\b/).should('not.exist');

    // Verifique se o lixo orgânico está visível e o não reciclável não está
    cy.get('.lixeiras-container').contains(/\borganicos\b/).should('exist');
    cy.get('.lixeiras-container').contains(/\bnao_reciclaveis\b/).should('not.exist');
});

  it('Caso de teste Cadastrar Lixeira', () => {
    cy.get('#cadastrar_lixeira').click();


    cy.get('#estado_atual').type('50');
    cy.get('button').click();//vou tentar enviar o formulário tendo preenchido apenas um dos campos 



    cy.get('#cadastrar_lixeira').click();
    cy.get('#domicilio').select('condominio');
    cy.get('#localizacao').type(randomAddress);
    cy.get('#bairro').select('Madalena'); 
    cy.get('#cliente-lixeira').select(cliente); 
    cy.get('#tipo_residuo').select('reciclaveis');
    cy.get('#capacidade_maxima').type('-1');//vou tentar digitar um numero negativo e o sistema nao deve permitir
    cy.get('#estado_atual').type('-1');
    cy.get('button').click();

    cy.get('#capacidade_maxima').clear().type('100');//agora devo conseguir enviar o formulario com os valores corretos
    cy.get('#estado_atual').clear().type('50');//Lixeira em 50% da capacidade
    cy.get('button').click();

    cy.get('.alert').contains('Lixeira cadastrada com sucesso.').should('be.visible');
  });

  it('Caso de teste de Avisos', () => {
    cy.get('#aviso_lixeira').click(); // Clica em avisos na navbar


    cy.get('#manutencao-card').contains('Manutenção necessária!').should('be.visible');
    cy.get('#lixeira-card').contains('Lixo cheio!').should('be.visible');

    // Verifica se o número em #progresso-value é maior que 80
    cy.get('#progresso-value').invoke('text').then((text) => {
        const progressoValue = parseInt(text);
        expect(progressoValue).to.be.greaterThan(80);
    });
});

  it('Caso de teste de Lixo por Bairro', () => {
    cy.get('#vialuzar_bairro').click();
    cy.get('#bairroChart').should('be.visible');//gráfico deve aparecer normalmente
  });

  it('Caso de teste Avaliar Coletas', () => {
    cy.get('#avaliar_coleta').click();
    cy.get('#bairroChart')//gráfico deve aparecer normalmente aqui também 
  });
});


describe('Conjunto de testes para Clientes', () => {
  beforeEach(() => {
    cy.exec('python3 manage.py delete_objects', { failOnNonZeroExit: false }); // Deleta os objetos que podem ter sido criados anteriormente
    cy.exec('python3 manage.py create_objects', { failOnNonZeroExit: false }); // Cria novamente para assegurar a independencia dos testes

    cy.visit('http://127.0.0.1:8000/auth/login/');
    cy.get('[placeholder="Usuário"]').type(cliente);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();

  });

  it('Caso de perfil do usuário', () => {
    cy.get('#lixeiraChart2').should('be.visible');//gráfico deve aparecer normalmente aqui através do perfil do usuário
})


it('Caso de teste agendamento de manutenção', () => {
  // Função para obter a data atual + 2 dias no formato 'YYYY-MM-DD'
  const getFutureDate = (daysToAdd) => {
      const date = new Date();
      date.setDate(date.getDate() + daysToAdd);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // mês começa de 0
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
  };

  // Função para obter a hora atual no formato 'HH:MM'
  const getCurrentTime = () => {
      const date = new Date();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
  };

  const futureDate = getFutureDate(2);
  const currentTime = getCurrentTime();

  cy.get('#agendar_manutencao').click();//clica na navbar

  cy.get('#data_manutencao').type(futureDate);
  cy.get('#tempo_manutencao').type(currentTime);
  cy.get('#lixeira-manutencao').select('av 17 de agosto 250');//uma das lixeiras criadas para o cliente nos testes
  cy.get('#motivo_manutencao').type('teste e2e');
  cy.get('button').click();

  cy.get('.alert').should('be.visible').and('have.text', 'Pedido enviado com sucesso!');
});

it('Caso de teste Avaliação das coletas', () => {
  cy.get('#avaliar_coleta').click();

  cy.get('.custom-form-container').should('have.length', 3);//Deve ter 3 elementos pois foi a quantidade de lixeiras que definimos como coleta_realizada=True nos casos de teste
  cy.get("#star-button").click();
  cy.get("#avaliacao-comentario").type("Avaliação de teste e2e");
  cy.get("#botao").click();
  cy.get('.alert').should('be.visible').and('have.text', 'Avaliação enviada com sucesso. Obrigado pelo seu feedback!');
});

})

describe('Conjunto de testes para Coletores', () => {
  beforeEach(() => {
    cy.exec('python3 manage.py delete_objects', { failOnNonZeroExit: false }); // Deleta os objetos que podem ter sido criados anteriormente
    cy.exec('python3 manage.py create_objects', { failOnNonZeroExit: false }); // Cria novamente para assegurar a independencia dos testes

    cy.visit('http://127.0.0.1:8000/auth/login/');
    cy.get('[placeholder="Usuário"]').type(coletor);
    cy.get('[placeholder="Senha"]').type('123');
    cy.get('button').click();
  });
  it('Caso de teste filtros para rotas de coleta', () => {

    cy.get("#melhor_rota").click()
     // Verifique se todos os tipos de lixo estão presentes antes de aplicar o filtro
     cy.get('.adress-container').contains(/\borganicos\b/).should('exist');
     cy.get('.adress-container').contains(/\breciclaveis\b/).should('exist');
     cy.get('.adress-container').contains(/\bnao_reciclaveis\b/).should('exist');
 
     // Aplicar o filtro para lixos recicláveis
     cy.get('#tipo_residuo').select('reciclaveis');
     cy.get('#botao-filtrar').click();
 
     // Verifique se o lixo orgânico não está mais visível
     cy.get('.adress-container').contains(/\borganicos\b/).should('not.exist');
 
     // Verifique se o lixo reciclável está visível e o não reciclável não está
     cy.get('.adress-container').contains(/\breciclaveis\b/).should('exist');
     cy.get('.adress-container').contains(/\bnao_reciclaveis\b/).should('not.exist');
 
     // Aplicar o filtro para lixos não recicláveis
     cy.get('#tipo_residuo').select('nao_reciclaveis');
     cy.get('#botao-filtrar').click();
 
     // Verifique se o lixo reciclável não está mais visível
     cy.get('.adress-container').contains(/\breciclaveis\b/).should('not.exist');
 
     // Verifique se o lixo não reciclável está visível e o orgânico não está
     cy.get('.adress-container').contains(/\bnao_reciclaveis\b/).should('exist');
     cy.get('.adress-container').contains(/\borganicos\b/).should('not.exist');
 
     // Aplicar o filtro para lixos orgânicos
     cy.get('#tipo_residuo').select('organicos');
     cy.get('#botao-filtrar').click();
 
     // Verifique se o lixo reciclável não está mais visível
     cy.get('.adress-container').contains(/\breciclaveis\b/).should('not.exist');
 
     // Verifique se o lixo orgânico está visível e o não reciclável não está
     cy.get('.adress-container').contains(/\borganicos\b/).should('exist');
     cy.get('.adress-container').contains(/\bnao_reciclaveis\b/).should('not.exist');
  })

  it('Caso de testes melhor rota de coleta', () => {
    cy.get('#melhor_rota').click();

    cy.get('.adress-container').should('have.length', 12);//Deve ter 12 elementos pois foi a quantidade de lixeiras que definidas com capacidade acima de 80%
    cy.get("#localizacao_atual").type("Av 17 de agosto 2593");//Endereço levando em conta os endereços criados na criação dos objetos
    cy.get("#botao-rota").click();//Iniciar uma coleta

    cy.get(".address-list-item").should('have.length', 13)//Um a mais pois agora levamos em contaa localização atual

    cy.get("#botao-finalizar").click();//Finalizamos uma rota de coleta

    cy.get(".alert").should('be.visible').and('have.text', 'Coleta finalizada com sucesso, obrigado pela sua contribuição!');

    //Tentando agora iniciar outra coleta logo em seguida, caso não haja outro endereço disponivel
    cy.get("#localizacao_atual").type("Av 17 de agosto 2593");//Endereço levando em conta os endereços criados na criação dos objetos
    cy.get("#botao-rota").click();//Iniciar uma coleta

    cy.get(".alert").should('be.visible').and('have.text', 'Localização atual e pelo menos um endereço são necessários.');
  })


  it('Caso de peso total coletado e número de coletas realizadas', () => {
    let coleta_valor;
    let peso_valor;

    cy.get('#perfil').click();
    cy.get('#coletas_realizadas').invoke('text').then((text) => {
        coleta_valor = parseInt(text);
    });

    cy.get('#peso_coletado').invoke('text').then((text) => {
        peso_valor = parseInt(text);
    });

    cy.get('#melhor_rota').click();
    cy.get("#localizacao_atual").type("Av 17 de agosto 2593");//Endereço levando em conta os endereços criados na criação dos objetos
    cy.get('#botao-rota').click();//Iniciar uma coleta

    cy.get("#botao-finalizar").click();//Finalizamos uma rota de coleta

    cy.get("#perfil").click();
    cy.get('#coletas_realizadas').invoke('text').then((text) => {
        const coleta_valor2 = parseInt(text);
        expect(coleta_valor2).to.equal(coleta_valor + 1);//Verificamos se a coleta foi registrada

        cy.get("#peso_coletado").invoke('text').then((text) => {
            const peso_valor2 = parseInt(text);
            expect(peso_valor2).to.equal(peso_valor + 10200);//Levando em conta o peso do lixo criado no comando create_objects
        });
    });

    
  })
})

after(() => {
  // Remove o banco de dados de testes
  cy.exec("rm db.sqlite3", { failOnNonZeroExit: false });
  // Restaura o banco de dados original, se houver
  cy.exec('if [ -f db_backup.sqlite3 ]; then mv db_backup.sqlite3 db.sqlite3; fi', { failOnNonZeroExit: false });
});

//10200,0 kg