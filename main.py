from playwright.sync_api import Playwright, sync_playwright
import pandas as pd

def kabum(palavra_chave):

    site = 'https://www.kabum.com.br'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(site)

        input = page.locator('[id="input-busca"]')
        input.fill(palavra_chave)

        b_pesquisa = page.locator('[class="sc-faCEWe sc-imaUOB esxRPr iPkCJu"]')
        b_pesquisa.click()

        # containers = class="sc-ff8a9791-7 JDtDP productCard"
        # nome = class="sc-d99ca57-0 bzucsr sc-ff8a9791-16 kMfyNu nameCard"
        # link = class="sc-ff8a9791-10 tEYzR"
        # preco = class="sc-3b515ca1-2 hQOqhY priceCard"

        data = []

        while True:

            page.wait_for_selector('[class="sc-d99ca57-0 bzucsr sc-ff8a9791-16 kMfyNu nameCard"]')

            p_containers = page.locator('[class="sc-ff8a9791-7 JDtDP productCard"]').all()

            for containers in p_containers:

                try:
                    nome = containers.locator('[class="sc-d99ca57-0 bzucsr sc-ff8a9791-16 kMfyNu nameCard"]').inner_text()
                    preco = containers.locator('[class="sc-3b515ca1-2 hQOqhY priceCard"]').inner_text()
                    link = containers.locator('[class="sc-ff8a9791-10 tEYzR"]').get_attribute('href')
                    print(f'Nome: {nome} Preco: {preco} Link: {link}')

                    data.append({"Produto": nome, "Preco": preco, "Link": site+link})

                except:
                    break

            try:
                next_page = page.locator('[class="nextLink"]')
                next_page.click()
                page.wait_for_selector('[class="sc-3b515ca1-2 hQOqhY priceCard"]')
            except:
                break

        df = pd.DataFrame(data)
        filename = f'kabum_{palavra_chave}.xlsx'
        df.to_excel(filename, index=False)
        print(f'{filename} / Quantidade de Produtos: {len(data)}')

if __name__ == '__main__':
    p_chave = input("Produto: ")
    kabum(p_chave)