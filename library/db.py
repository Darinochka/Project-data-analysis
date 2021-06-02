    # -*- coding: utf-8 -*-
"""
Сохранение данных в файле
Автор: Поляков К. Л.
"""
# Тестовая база
def base1():
    """
    Учебная база данных сотрудников
    Параметров нет
    Возвращает словарь словарей
    Указано количество детей
    Автор: Поляков К. Л. 
    """
    fields = ["имя", "пол", "возраст", "зарплата", "дети", "департамент"]
    surname = ["Иванов", "Сидоров", "Чернова", "Корюшка", "Берг", "Климов"]
    Иванов = ["Павел Иванов", "муж", 42, 30000, 0, "маркетинг"]
    Сидоров = ["Юрий Сидоров", "муж", 32, 35000, 3, "финансы"]
    Чернова = ["Татьяна Чернова", "жен", 53, 40000, 10, "продажи"]
    Корюшка = ["Ирина Корюшка", "жен", 23, 20000, 2, "маркетинг"]
    Берг = ["Игорь Берг", "муж", 33, 25000, 6, "продажи"]
    Климов = ["Андрей Климов", "муж", 60, 60000, 0, "финансы"]
# Создаем список списков
    w1 = [Иванов, Сидоров, Чернова, Корюшка, Берг, Климов]
# Создаем списко словарей
    w2 = [dict(zip(fields,x)) for x in w1]
# Создаем словарь словарей
    w3 = dict(zip(surname, w2))
    return w3

def base2():
    """
    Учебная база данных сотрудников
    Параметров нет
    Возвращает словарь словарей
    Указан возраст каждого ребенка в списке
    Автор: Поляков К. Л. 
    """
    fields = ["имя", "пол", "возраст", "зарплата", "дети", "департамент"]
    surname = ["Иванов", "Сидоров", "Чернова", "Корюшка", "Берг", "Климов"]
    Иванов = ["Павел Иванов", "муж", 42, 30000, [], "маркетинг"]
    Сидоров = ["Юрий Сидоров", "муж", 32, 35000, [2,4,10], "финансы"]
    Чернова = ["Татьяна Чернова", "жен", 53, 40000, list(range(2,10)), "продажи"]
    Корюшка = ["Ирина Корюшка", "жен", 23, 20000, [5,7], "маркетинг"]
    Берг = ["Игорь Берг", "муж", 33, 25000, list(range(3,9)), "продажи"]
    Климов = ["Андрей Климов", "муж", 60, 60000, [], "финансы"]
# Создаем список списков
    w1 = [Иванов, Сидоров, Чернова, Корюшка, Берг, Климов]
# Создаем списко словарей
    w2 = [dict(zip(fields,x)) for x in w1]
# Создаем словарь словарей
    w3 = dict(zip(surname, w2))
    return w3

def base3():
    """
    Учебная база данных сотрудников
    Входных параметров нет
    Возвращает словарь словарей
    Указан пол и возраст каждого ребенка в словаре
    Автор: Поляков К. Л.
    """
    fields = ["имя", "пол", "возраст", "зарплата", "дети", "департамент"]
    surname = ["Иванов", "Сидоров", "Чернова", "Корюшка", "Берг", "Климов"]
    Иванов = ["Павел Иванов", "муж", 42, 30000, {"мальчики":[], "девочки":[]}, "маркетинг"]
    Сидоров = ["Юрий Сидоров", "муж", 32, 35000, {"мальчики":[2, 4], "девочки":[10]}, "финансы"]
    Чернова = ["Татьяна Чернова", "жен", 53, 40000, {"мальчики":[3], "девочки":[5, 6, 7]},
               "продажи"]
    Корюшка = ["Ирина Корюшка", "жен", 23, 20000, {"мальчики":[], "девочки":[3, 10]}, "маркетинг"]
    Берг = ["Игорь Берг", "муж", 33, 25000, {"мальчики":[5, 6], "девочки":[]}, "продажи"]
    Климов = ["Андрей Климов", "муж", 60, 60000, {"мальчики":[4], "девочки":[3]}, "финансы"]
# Создаем список списков
    w1 = [Иванов, Сидоров, Чернова, Корюшка, Берг, Климов]
# Создаем списко словарей
    w2 = [dict(zip(fields, x)) for x in w1]
# Создаем словарь словарей
    w3 = dict(zip(surname, w2))
    return w3
