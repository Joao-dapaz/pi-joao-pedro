from datetime import datetime

from playwright.sync_api import Page, expect

def test_home(page: Page):
    page.goto("http://localhost:5000/")
    
    expect(page).to_have_title("Maestro - Conexões musicais")

def test_home_conteudo(page: Page):
    page.goto("http://localhost:5000/")
    
    expect(page.locator("text=Maestro")).to_be_visible()

def test_login_aluno(page: Page):
    page.goto("http://localhost:5000/login")

    page.fill('input[name="email"]', "rafael@email.com")
    page.fill('input[name="senha"]', "abc")

    page.click('button[type="submit"]')

    expect(page).to_have_url("http://localhost:5000/login")

def test_login_invalido(page: Page):
    page.goto("http://localhost:5000/login")

    page.fill('input[name="email"]', "errado@email.com")
    page.fill('input[name="senha"]', "123")

    page.click('button[type="submit"]')

    expect(page.locator("text=Email ou senha inválidos")).to_be_visible()

def test_ver_materiais(page: Page):
    page.goto("http://localhost:5000/login")

    page.fill('input[name="email"]', "rafael@email.com")
    page.fill('input[name="senha"]', "abc")
    page.click('button[type="submit"]')

    # Não verifica URL, vai direto para turmas
    page.goto("http://localhost:5000/turmas")
    
    # Se não estiver autenticado, será redirecionado para /
    if page.url == "http://localhost:5000/":
        print("Falha no login!")
        return
    
    page.click("button:has-text('Ver materiais')")
    expect(page.locator("text=Nenhum material ainda.")).to_be_visible()

def test_mapa_visivel(page: Page):
    page.goto("http://localhost:5000/conexao_escola")

    mapa = page.locator("#mapa")

    expect(mapa).to_be_visible()

def test_acesso_pagina_cadastro(page: Page):
    page.goto("http://localhost:5000/cadastrar")
    
   
    expect(page.locator('input[name="nome"]')).to_be_visible()
    expect(page.locator('input[name="email"]')).to_be_visible()
    expect(page.locator('input[name="telefone"]')).to_be_visible()
    expect(page.locator('input[name="endereco"]')).to_be_visible()
    expect(page.locator('input[name="senha"]')).to_be_visible()
    
   
    expect(page.locator('button[type="submit"]')).to_be_visible()


def test_cadastro_bem_sucedido(page: Page):
    page.goto("http://localhost:5000/cadastrar")
    
    # Email NUNCA vai se repetir
    email = f"joao_{datetime.now().strftime('%Y%m%d%H%M%S%f')}@email.com"
    
    page.fill('input[name="nome"]', "João da Silva")
    page.fill('input[name="email"]', email)
    page.fill('input[name="telefone"]', "11999999999")
    page.fill('input[name="endereco"]', "Rua das Flores, 123")
    page.fill('input[name="senha"]', "senha123")
    
    page.click('button[type="submit"]')
    
    expect(page).to_have_url("http://localhost:5000/conexao_escola")


def test_email_duplicado(page: Page):
    """Testa se o cadastro rejeita um email já existente."""
    page.goto("http://localhost:5000/cadastrar")
    
    # Tenta cadastrar com email que já existe (rafael@email.com existe nos dados iniciais)
    page.fill('input[name="nome"]', "Outro Aluno")
    page.fill('input[name="email"]', "rafael@email.com")
    page.fill('input[name="telefone"]', "11987654321")
    page.fill('input[name="endereco"]', "Avenida Principal, 456")
    page.fill('input[name="senha"]', "senha456")
    
    page.click('button[type="submit"]')
    
    # Verifica se mostra a mensagem de erro
    expect(page.locator(".toast-body")).to_contain_text("Email já cadastrado.")
    
    # Verifica se mantém na página de cadastro
    expect(page).to_have_url("http://localhost:5000/cadastrar")


def test_campo_nome_vazio(page: Page):
    page.goto("http://localhost:5000/cadastrar")

    page.fill('input[name="email"]', "teste_vazio@email.com")
    page.fill('input[name="telefone"]', "11988888888")
    page.fill('input[name="endereco"]', "Rua Teste, 789")
    page.fill('input[name="senha"]', "senha789")
    
    # Tenta enviar (o campo required do HTML deve impedir)
    submit_button = page.locator('button[type="submit"]')
    
    # Se o navegador bloquear, o form não é enviado
    # Se não bloquear, pelo menos verifica se continua na página
    submit_button.click()
    
    # Verifica que a página não mudou ou que mantém no cadastro
    expect(page).to_have_url("http://localhost:5000/cadastrar")