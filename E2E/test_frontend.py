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

    page.goto("http://localhost:5000/turmas")

    page.click("text=Ver materiais")

    expect(page.locator("text=Nenhum material ainda.")).to_be_visible()

def test_mapa_visivel(page: Page):
    page.goto("http://localhost:5000/conexao_escola")

    mapa = page.locator("#mapa")

    expect(mapa).to_be_visible()