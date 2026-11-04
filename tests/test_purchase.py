import pytest
import time
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

#Фикстура для авторизации с валидными данными
@pytest.fixture
def logged_in_driver(driver):
    #Ищем поле для ввода логина и заполняем его валидным значением ("standard_user")
    with allure.step('Предусловие: авторизация в системе'):
        driver.find_element(*locators_file.USER_NAME).send_keys("standard_user")
        #Ищем поле для ввода пароля и заполняем его валидным значением ("secret_sauce")
        driver.find_element(*locators_file.PASSWORD).send_keys("secret_sauce")
        #Ищем кнопку для входа и кликаем на нее
        driver.find_element(*locators_file.LOGIN_BUTTON).click()
        #Ждем пока появится возможность перейти в корзину (для последующей предварительной очистки корзины),
        #максимальное время ожидание - 10 секунд
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.SHOPPING_CART_LINK))
    #Возвращаем переменную браузера
    return driver

#Фикстура для очистки корзины и перехода обратно к каталогу
@pytest.fixture
def clean_cart(logged_in_driver):
    with allure.step('Предусловие: предварительная очистка корзины'):
        #Переход в корзину
        logged_in_driver.find_element(*locators_file.SHOPPING_CART_LINK).click()
        #Ждем пока кнопка для возвращения из корзины обратно в каталог станет кликабельной, максимальное время ожидание - 10 секунд,
        #(в корзине могут быть товары, а, возможно, она пустая, поэтому, чтобы понять, что страница корзины загрузилась -
        #ориентируемся на кнопку для возврата обратно в каталог, так как она будет в любом случае)
        continue_shopping = WebDriverWait(logged_in_driver, 10).until(EC.element_to_be_clickable(locators_file.CONTINUE_SHOPPING))
        #Ищем все кнопки для удаления товара из корзины
        remove_buttons = logged_in_driver.find_elements(*locators_file.REMOVE_BUTTONS)
        #Кликаем по всем найденным кнопкам для удаления товара из корзины
        for btn in remove_buttons:
            btn.click()
            time.sleep(0.3)
        #Кликаем на кнопку возврата к каталогу
        continue_shopping.click()
    #Возвращаем переменную браузера
    return logged_in_driver

#Определяю главную область, к которой относится тест
@allure.feature('Работа с товарами')
#Описываю конкретный случай, в котором используется тест
@allure.story('Покупка товаров')
#Задаю заголовок теста
@allure.title('Проверка успешной покупки рюкзака')
#Определяю уровень критичности теста
@allure.severity(allure.severity_level.CRITICAL)
#Указываю дополнительную метку (под какой учетной записью проводится тест)
@allure.label('user_name','standard_user')
#Тест для проверки успешной покупки товара
def test_purchase_backpack(clean_cart):
    driver = clean_cart
    #Ждем пока кнопка для добавления рюкзака в корзину станет кликабельной и кликаем по ней,
    #максимальное время ожидание - 10 секунд
    with allure.step('Добавление товара в корзину и переход к первому шагу оформления заказа'):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.ADD_TO_CART_BACKPACK)).click()
        #Переходим в корзину
        driver.find_element(*locators_file.SHOPPING_CART_LINK).click()
        #Ждем пока кнопка для перехода к первому шагу оформления заказа (заполнению данных) станет кликабельной и кликаем по ней,
        #максимальное время ожидание - 10 секунд
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.CHECKOUT)).click()
    with allure.step('Первый шаг оформления заказа и переход к второму шагу'):
        #Ждем пока кнопка для перехода к второму шагу оформления заказа станет кликабельной,
        #максимальное время ожидание - 10 секунд
        move_to_second_step = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.CONTINUE))
        #Ищем поле для ввода имени и заполняем его
        driver.find_element(*locators_file.FIRST_NAME).send_keys("Ivan")
        #Ищем поле для ввода фамилии и заполняем его
        driver.find_element(*locators_file.LAST_NAME).send_keys("Ivanov")
        #Ищем поле для ввода zip/postal кода и заполняем его
        driver.find_element(*locators_file.POSTAL_CODE).send_keys("0000")
        #Переходим к второму шагу оформления заказа
        move_to_second_step.click()
    with allure.step('Окончание оформления заказа и проверка успешного завершения покупки'):
        #Ждем пока кнопка для подтверждения покупки станет кликабельной и кликаем по ней,
        #максимальное время ожидание - 10 секунд
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.FINISH)).click()
        time.sleep(1)
        #Проверяем успешное завершение покупки, для этого проверяем наличие кнопки для генерации чека на покупку.
        #Логика такая: если есть кнопка для генерации чека на покупку, то, следовательно, покупка успешно завершена
        generate_pdf_order = driver.find_elements(*locators_file.GENERATE_PDF_ORDER)
        assert len(generate_pdf_order) == 1, 'Не удалось успешно завершить покупку'
    print('Успешная покупка пройдена')