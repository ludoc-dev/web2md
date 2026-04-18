# pages/article_page.py - Page Object para páginas de artigo
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ArticlePage(BasePage):
    """Page Object para páginas de artigo com conteúdo principal"""

    # Locators
    TITLE = (By.TAG_NAME, "h1")
    CONTENT = (By.TAG_NAME, "article")
    MAIN_CONTENT = (By.CSS_SELECTOR, "main")
    PARAGRAPHS = (By.TAG_NAME, "p")
    LINKS = (By.TAG_NAME, "a")
    CODE_BLOCKS = (By.TAG_NAME, "pre")
    NAVIGATION = (By.TAG_NAME, "nav")
    SIDEBAR = (By.TAG_NAME, "aside")
    FOOTER = (By.TAG_NAME, "footer")

    def get_title(self) -> str:
        """Retorna título principal do artigo"""
        return self.get_text(self.TITLE)

    def get_content(self) -> str:
        """Retorna conteúdo do artigo"""
        element = self.find_element(self.CONTENT)
        return element.text

    def get_main_content(self) -> str:
        """Retorna conteúdo principal"""
        element = self.find_element(self.MAIN_CONTENT)
        return element.text

    def get_paragraphs(self) -> list[str]:
        """Retorna todos os parágrafos"""
        elements = self.find_elements(self.PARAGRAPHS)
        return [elem.text for elem in elements if elem.text.strip()]

    def get_links(self) -> list[dict]:
        """Retorna todos os links com href e texto"""
        elements = self.find_elements(self.LINKS)
        links = []
        for elem in elements:
            href = elem.get_attribute("href")
            text = elem.text
            if href:
                links.append({"href": href, "text": text})
        return links

    def get_code_blocks(self) -> list[str]:
        """Retorna todos os code blocks"""
        elements = self.find_elements(self.CODE_BLOCKS)
        return [elem.text for elem in elements if elem.text.strip()]

    def has_navigation(self) -> bool:
        """Verifica se tem navegação"""
        return self.is_visible(self.NAVIGATION, timeout=2)

    def has_sidebar(self) -> bool:
        """Verifica se tem sidebar"""
        return self.is_visible(self.SIDEBAR, timeout=2)

    def has_footer(self) -> bool:
        """Verifica se tem footer"""
        return self.is_visible(self.FOOTER, timeout=2)

    def count_noise_elements(self) -> int:
        """Conta elementos de ruído (nav, sidebar, footer, ads)"""
        noise_count = 0
        if self.has_navigation():
            noise_count += 1
        if self.has_sidebar():
            noise_count += 1
        if self.has_footer():
            noise_count += 1
        return noise_count

    def get_content_length(self) -> int:
        """Retorna tamanho do conteúdo principal"""
        return len(self.get_main_content())

    def is_valid_article(self) -> bool:
        """Verifica se é um artigo válido"""
        has_title = self.is_visible(self.TITLE, timeout=2)
        has_content = self.is_visible(self.CONTENT, timeout=2) or self.is_visible(self.MAIN_CONTENT, timeout=2)
        return has_title and has_content
