# pages/elements.py - Elementos mapeados para Selenium
from selenium.webdriver.common.by import By

class CommonElements:
    """Elementos comuns em páginas web"""

    # Headers
    H1 = (By.TAG_NAME, "h1")
    H2 = (By.TAG_NAME, "h2")
    H3 = (By.TAG_NAME, "h3")

    # Content
    PARAGRAPH = (By.TAG_NAME, "p")
    LIST_ITEM = (By.TAG_NAME, "li")
    ORDERED_LIST = (By.TAG_NAME, "ol")
    UNORDERED_LIST = (By.TAG_NAME, "ul")

    # Links
    LINK = (By.TAG_NAME, "a")
    EXTERNAL_LINK = (By.CSS_SELECTOR, "a[href^='http']")

    # Code
    CODE_BLOCK = (By.TAG_NAME, "pre")
    INLINE_CODE = (By.TAG_NAME, "code")
    CODE = (By.CSS_SELECTOR, "pre code")

    # Structure
    NAVIGATION = (By.TAG_NAME, "nav")
    SIDEBAR = (By.TAG_NAME, "aside")
    MAIN = (By.TAG_NAME, "main")
    ARTICLE = (By.TAG_NAME, "article")
    FOOTER = (By.TAG_NAME, "footer")
    HEADER = (By.TAG_NAME, "header")

    # Forms
    BUTTON = (By.TAG_NAME, "button")
    INPUT = (By.TAG_NAME, "input")
    FORM = (By.TAG_NAME, "form")

    # Media
    IMAGE = (By.TAG_NAME, "img")
    VIDEO = (By.TAG_NAME, "video")
    AUDIO = (By.TAG_NAME, "audio")

    # Tables
    TABLE = (By.TAG_NAME, "table")
    TABLE_ROW = (By.TAG_NAME, "tr")
    TABLE_CELL = (By.TAG_NAME, "td")
    TABLE_HEADER = (By.TAG_NAME, "th")

    # Metadata
    TITLE = (By.TAG_NAME, "title")
    META_DESCRIPTION = (By.CSS_SELECTOR, "meta[name='description']")
    META_KEYWORDS = (By.CSS_SELECTOR, "meta[name='keywords']")

class NoiseElements:
    """Elementos considerados ruído"""

    # Ads
    AD_BANNER = (By.CSS_SELECTOR, ".ad, .advertisement, .banner")
    AD_IFRAME = (By.CSS_SELECTOR, "iframe[src*='ad']")

    # Social
    SOCIAL_SHARE = (By.CSS_SELECTOR, ".social-share, .share-buttons")
    COMMENTS = (By.CSS_SELECTOR, ".comments, #comments")

    # Navigation
    MENU = (By.CSS_SELECTOR, ".menu, .navbar, .navigation")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")

    # Sidebars
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar, aside")
    WIDGET = (By.CSS_SELECTOR, ".widget")

class ContentElements:
    """Elementos de conteúdo principal"""

    # Article content
    ARTICLE_BODY = (By.CSS_SELECTOR, "article p, .content, .post-content")
    ARTICLE_TITLE = (By.CSS_SELECTOR, "article h1, .entry-title, .post-title")

    # Documentation
    DOC_CONTENT = (By.CSS_SELECTOR, ".docs-content, .documentation, main")
    DOC_TITLE = (By.CSS_SELECTOR, "h1, .page-title, .docs-title")

    # Blog
    BLOG_POST = (By.CSS_SELECTOR, ".blog-post, .post, article")
    BLOG_TITLE = (By.CSS_SELECTOR, ".entry-title, .post-title, h1")

    @staticmethod
    def main_content_selectors():
        """Retorna seletores CSS para conteúdo principal"""
        return [
            "main",
            "article",
            "[role='main']",
            ".content",
            ".post-content",
            ".entry-content",
            "#content",
            ".documentation",
            ".docs-content"
        ]
