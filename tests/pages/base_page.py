# pages/base_page.py - Page Object base para Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Page Object base com métodos comuns"""

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.timeout = 10

    def open(self, url: str):
        """Abre URL na página"""
        self.driver.get(url)

    def find_element(self, locator: tuple, timeout: int = None):
        """Encontra elemento com wait explícito"""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: tuple, timeout: int = None):
        """Encontra múltiplos elementos"""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator: tuple):
        """Clica em elemento"""
        element = self.find_element(locator)
        element.click()

    def get_text(self, locator: tuple) -> str:
        """Retorna texto de elemento"""
        element = self.find_element(locator)
        return element.text

    def is_visible(self, locator: tuple, timeout: int = None) -> bool:
        """Verifica se elemento está visível"""
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_page_load(self, timeout: int = None):
        """Aguarda página carregar completamente"""
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def get_page_title(self) -> str:
        """Retorna título da página"""
        return self.driver.title

    def get_url(self) -> str:
        """Retorna URL atual"""
        return self.driver.current_url

    def scroll_to_element(self, locator: tuple):
        """Scroll até elemento"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def take_screenshot(self, filename: str):
        """Tira screenshot da página"""
        self.driver.save_screenshot(filename)
