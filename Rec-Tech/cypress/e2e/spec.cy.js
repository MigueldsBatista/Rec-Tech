describe('test suite 1', () => {
  it('Register', () => {
    cy.visit('/');
    cy.get('a').click()
    cy.get('[type="text"]').type('teste')
    cy.get('[type="email"]').type('email@teste.com')
    cy.get(':nth-child(3) > .form-control').type('123')
    cy.get('#user-type').select('admin')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .form-control').type('teste')
    cy.get(':nth-child(3) > .form-control').type('123')
    cy.get('.btn').click()
    cy.get('.alert').invoke('text').should('have.string', "Your account has been created")



    })
  it('Login', () => {
  })





  it('cenario3', () => {
      //steps do cenario3
  })
})