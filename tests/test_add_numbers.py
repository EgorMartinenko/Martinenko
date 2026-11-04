#Импорт pytest
import pytest
#Импорт функции add_numbers, которую нужно протестировать
from add_numbers import add_numbers

#Параметризованная фикстура
@pytest.fixture(params=[
    #Два положительных числа и результат их сложения
    ((5, 7), 12),
    #Три числа с разными знаками и результат их сложения
    ((2, -8, 12), 6),
    #Более трех чисел с разными знаками и результат их сложения
    ((-5, 20, 1, -9, 9, -4), 12),
    #Несколько чисел, включая нули и результат их сложения
    ((13, 0, -2, 23, 14, -9, 0, 12), 51)
])
def test_add_numbers_data(request):
    return request.param

#Тест
@pytest.mark.skip
def test_add_numbers(test_add_numbers_data):
    #Достаем кортеж с набором чисел и число результат их сложения
    numbers, result = test_add_numbers_data
    #Сравниваем
    assert add_numbers(*numbers) == result