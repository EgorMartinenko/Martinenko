import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#Импорт файла с локаторами, найденными в практической работе №6
from selenium_tests.locators import locators_file
import allure

#Фикстура для запуска браузера в режиме инкогнито и последующего закрытия сессии браузера
@pytest.fixture
def driver():
    #Создаем объект options для браузера
    options = Options()
    #Добавляем объекту options аргумент --incognito, чтобы браузер запускался в режиме инкогнито
    options.add_argument("--incognito")
    #Путь к обновленному chrome
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    #Создаем объект service для браузера и скачиваем драйвер для браузера
    service = Service(ChromeDriverManager().install())
    #Создаем переменную driver и передаем в нее аргументы service и options, которые создали ранее (запускаем браузер)
    driver = webdriver.Chrome(service=service, options=options)
    #Разворачиваем окно браузера на весь экран
    driver.maximize_window()
    #Переходим по ссылке
    driver.get("https://www.saucedemo.com/")
    #Возвращаем переменную браузера
    yield driver
    #После окончания работы закрываем сессию браузера
    driver.quit()

#Определяю главную область, к которой относится тест
@allure.feature('Авторизация')
#Описываю конкретный случай, в котором используется тест
@allure.story('Авторизация с невалидными данными')
#Задаю заголовок теста
@allure.title('Авторизация с невалидными логином и паролем')
#Определяю уровень критичности теста
@allure.severity(allure.severity_level.NORMAL)
#Указываю дополнительную метку (под какой учетной записью проводится тест)
@allure.label('user','Ivan_user (invalid)')
#Тест для проверки неуспешной авторизации
def test_unsuccessful_auth(driver):
    with allure.step('Ввод невалидных логина, пароля и попытка входа'):
        #Ищем поле для ввода логина и заполняем его невалидным значением ("Ivan_user")
        driver.find_element(*locators_file.USER_NAME).send_keys("Ivan_user")
        #Ищем поле для ввода пароля и заполняем его невалидным значением ("Ivan_password")
        driver.find_element(*locators_file.PASSWORD).send_keys("Ivan_password")
        #Ищем кнопку для входа и кликаем на нее
        driver.find_element(*locators_file.LOGIN_BUTTON).click()
    with allure.step('Получение текста сообщения об ошибке и проверка корректности данного текста'):
        #Ожидаем когда появится сообщение об ошибке и проверяем текст этого сообщения
        error_message = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.ERROR_MESSAGE_CONTAINER)).text
        assert error_message == "Epic sadface: Username and password do not match any user in this service",\
        'Система некорректно среагировала на неуспешную авторизацию'
    print('Неуспешная авторизация успешно пройдена')