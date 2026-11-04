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

#Определяю главную область, к которой относится тест
@allure.feature('Работа с товарами')
#Описываю конкретный случай, в котором используется тест
@allure.story('Управление товарами в корзине')
#Задаю заголовок теста
@allure.title('Проверка успешного очищения корзины')
#Определяю уровень критичности теста
@allure.severity(allure.severity_level.CRITICAL)
#Указываю дополнительную метку (под какой учетной записью проводится тест)
@allure.label('user','Standard User')
#Тест для проверки очищения корзины
def test_clean_cart(logged_in_driver):
    driver = logged_in_driver
    #Ждем пока кнопка для добавления рюкзака в корзину станет кликабельной и кликаем по ней,
    #максимальное время ожидание - 10 секунд
    with allure.step('Добавление товара в корзину и переход в нее'):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators_file.ADD_TO_CART_BACKPACK)).click()
        #Переходим в корзину
        driver.find_element(*locators_file.SHOPPING_CART_LINK).click()
    with allure.step('Очистка корзины'):
        #Ищем все кнопки для удаления товара из корзины
        remove_buttons = driver.find_elements(*locators_file.REMOVE_BUTTONS)
        # Кликаем по всем найденным кнопкам для удаления товара из корзины
        for btn in remove_buttons:
            btn.click()
            time.sleep(1)
    with allure.step('Проверка того, что в корзине больше нет товаров'):
        # Проверяем, что в корзине больше нет товаров
        cart_items = driver.find_elements(*locators_file.CART_ITEM)
        assert len(cart_items) == 0, 'Не удалось успешно очистить корзину'
    #Переходим обратно в каталог (в задание требуется проверить еще и успешное возвращение в каталог)
    with allure.step('Проверка успешного перехода обратно в каталог'):
        driver.find_element(*locators_file.CONTINUE_SHOPPING).click()
        #Проверяем наличие кнопки для добавления рюкзака в корзину (если такая кнопка есть - значит мы успешно вернулись в каталог)
        add_to_cart_backpack_buttons = driver.find_elements(*locators_file.ADD_TO_CART_BACKPACK)
        assert len(add_to_cart_backpack_buttons) == 1, 'Не удалось успешно вернуться в каталог'
    print('Очистка корзины успешной пройдена')