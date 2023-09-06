
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager(version="114.0.5735.90").install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()




# @pytest.fixture(params=["Chrome", "Firefox", "Edge"])
# def setup(request):
#     if request.param == "Chrome":
#         from selenium import webdriver
#         from selenium.webdriver.chrome.service import Service
#         from selenium.webdriver.chrome.options import Options
#         from webdriver_manager.chrome import ChromeDriverManager
#         chrome_options = Options()
#         chrome_options.add_experimental_option("detach", True)
#         service_obj = Service(ChromeDriverManager(version="115.0.5790.114").install())
#         driver = webdriver.Chrome(service=service_obj, options=chrome_options)
#         return driver
#     elif request.param == "Firefox":
#         from selenium import webdriver
#         from selenium.webdriver.firefox.service import Service
#         from selenium.webdriver.firefox.options import Options
#         from webdriver_manager.firefox import GeckoDriverManager
#         firefox_options = Options()
#         firefox_options.set_capability("moz:firefoxOptions", {"detach": True})
#         service_obj = Service(GeckoDriverManager(version="115.0.5790.114").install())
#         driver = webdriver.Firefox(service=service_obj, options=firefox_options)
#         return driver
#     elif request.param == "Edge":
#         from selenium import webdriver
#         from selenium.webdriver.edge.service import Service
#         from selenium.webdriver.edge.options import Options
#         from webdriver_manager.microsoft import EdgeChromiumDriverManager
#         edge_options = webdriver.EdgeOptions()
#         edge_options.set_capability("edgeOptions", {"detach": True})
#         service_obj = Service(EdgeChromiumDriverManager(version="115.0.5790.114").install())
#         driver = webdriver.Edge(service=service_obj, options=edge_options)
#         return driver
