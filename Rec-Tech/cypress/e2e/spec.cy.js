describe('test suite 1', () => {
  let randomEmail;
  let randomName;
  let randomAdress;
  let randomDecimal;
  let sub_randomDecimal;


  before(() => {
    // Gera um email e um nome aleatórios
    const randomString = Math.random().toString(36).substring(2, 11);
    randomEmail = `user_${randomString}@test.com`;
    randomName = `Name_${randomString}`;
  });


  describe('Test Suite for Multiple User Types', () => {
    let randomEmail;
    let randomName;


    beforeEach(() => {
      // Gera um email e um nome aleatórios
      const randomString = Math.random().toString(36).substring(2, 11);
      const randomNumber = Math.floor(Math.random() * 1000) + 1;


      randomAdress = `Av 17 de agosto ${randomNumber}`


      randomEmail = `user_${randomString}@test.com`;
      randomName = `Name_${randomString}`;
      randomDecimal = randomNumber.toFixed(0)
      sub_randomDecimal=randomNumber*0.85.toFixed(0)
    });


    it('Register as Admin', () => {
      cy.visit('/');
      cy.get('a').click();
      cy.get('[type="text"]').type(randomName); // Usa o nome gerado
      cy.get('[type="email"]').type(randomEmail); // Usa o email gerado
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('#user-type').select('admin'); // Define o tipo como 'admin'
      cy.get('.btn').click();
      cy.get(':nth-child(2) > .form-control').type(randomName); // Reutiliza o mesmo nome
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('.btn').click();


      //Dentro da página do admin
      cy.get(':nth-child(1) > .nav-link').click()
      cy.get(':nth-child(2) > .nav-link').click()
      cy.get('#domicilio').select('condominio')
      cy.get('#localizacao').type(randomAdress)
      cy.get('#email').type(randomEmail)
      cy.get('#tipo_residuo').select('reciclaveis')
      cy.get('#capacidade_maxima').type(randomDecimal)
      cy.get('#estado_atual').type(sub_randomDecimal)
      cy.get('#senha').type('123')
      cy.get('.btn').click()
    });


    it('Register as Collector', () => {
      cy.visit('/');
      cy.get('a').click();
      cy.get('[type="text"]').type(randomName); // Usa o nome gerado
      cy.get('[type="email"]').type(randomEmail); // Usa o email gerado
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('#user-type').select('coletor'); // Define o tipo como 'collector'
      cy.get('.btn').click();
      cy.visit('/');
      cy.get(':nth-child(2) > .form-control').type(randomName); // Reutiliza o mesmo nome
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('.btn').click();
      //Dentro da página do coletor
      cy.get('p > .btn')
      cy.get('#localizacao_atual').type(randomAdress)
      cy.get('.mt-3 > .btn').click()
     
     


    });


    it('Register as Client', () => {
      cy.visit('/');
      cy.get('a').click();
      cy.get('[type="text"]').type(randomName); // Usa o nome gerado
      cy.get('[type="email"]').type(randomEmail); // Usa o email gerado
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('#user-type').select('cliente'); // Define o tipo como 'client'
      cy.get('.btn').click();
      cy.visit('/');
      cy.get(':nth-child(2) > .form-control').type(randomName); // Reutiliza o mesmo nome
      cy.get(':nth-child(3) > .form-control').type('123');
      cy.get('.btn').click();
    });


    it('Scenario 3', () => {
      // Passos para o cenário 3
    });
  });




  it('cenario3', () => {
    // Insira os passos para o cenário 3
  });
});



