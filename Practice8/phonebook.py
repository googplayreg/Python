import psycopg2
from connect import get_connection

# ==========================================
# 0. СОЗДАНИЕ ТАБЛИЦЫ
# ==========================================
def create_phonebook_table():
    """Создает таблицу contacts с правильными уникальными ограничениями"""
    conn = get_connection()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contacts (
                        contact_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        phone_number VARCHAR(20) NOT NULL,
                        UNIQUE (first_name, last_name) -- Важно для UPSERT!
                    );
                """)
                conn.commit()
                print('Таблица "contacts" готова к работе.')
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            conn.close()

# ==========================================
# 1. ПОИСК ПО ПАТТЕРНУ
# ==========================================
def find_contacts(pattern):
    sql = "SELECT * FROM get_contacts_by_pattern(%s);"
    conn = None
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (pattern,))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при поиске: {error}")
    finally:
        if conn is not None:
            conn.close()
    return rows

# ==========================================
# 2. ДОБАВЛЕНИЕ / ОБНОВЛЕНИЕ (UPSERT)
# ==========================================
def save_contact(first_name, last_name, phone):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s, %s)", (first_name, last_name, phone))
        conn.commit()
        print(f"Контакт {first_name} {last_name} успешно сохранен/обновлен.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при сохранении: {error}")
        if conn: conn.rollback()
    finally:
        if conn is not None:
            conn.close()

# ==========================================
# 3. МАССОВАЯ ВСТАВКА
# ==========================================
def insert_batch(contacts_list):
    if not contacts_list:
        return
        
    f_names = [c[0] for c in contacts_list]
    l_names = [c[1] for c in contacts_list]
    phones = [c[2] for c in contacts_list]
    
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        errors = ""
        
        cur.execute("CALL insert_many_contacts(%s, %s, %s, %s)", (f_names, l_names, phones, errors))
        result_errors = cur.fetchone()[0]
        conn.commit()
        
        if result_errors:
            print("\nЗавершено с предупреждениями (неверный формат номеров):")
            print(result_errors)
        else:
            print("\nВсе контакты успешно добавлены!")
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка массовой вставки: {error}")
        if conn: conn.rollback()
    finally:
        if conn is not None:
            conn.close()

# ==========================================
# 4. ПАГИНАЦИЯ (ПОСТРАНИЧНЫЙ ВЫВОД)
# ==========================================
def get_page(page_number, size=5):
    offset = (page_number - 1) * size
    sql = "SELECT * FROM get_contacts_paged(%s, %s);"
    conn = None
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (size, offset))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка пагинации: {error}")
    finally:
        if conn is not None:
            conn.close()
    return rows

# ==========================================
# 5. УДАЛЕНИЕ
# ==========================================
def remove_contact(name=None, phone=None):
    if not name and not phone:
        print("Ошибка: нужно указать имя или телефон для удаления.")
        return

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CALL delete_contact(%s, %s)", (name, phone))
        conn.commit()
        print("Запрос на удаление выполнен.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при удалении: {error}")
        if conn: conn.rollback()
    finally:
        if conn is not None:
            conn.close()

# ==========================================
# ИНТЕРАКТИВНОЕ МЕНЮ
# ==========================================
def main():
    # При запуске скрипта убеждаемся, что таблица существует
    create_phonebook_table()
    
    while True:
        print("\n" + "="*30)
        print(" ТЕЛЕФОННАЯ КНИГА (Advanced)")
        print("="*30)
        print("1. Найти контакт")
        print("2. Добавить или обновить контакт")
        print("3. Множественное добавление контактов")
        print("4. Показать все (постранично)")
        print("5. Удалить контакт")
        print("0. Выход")
        print("="*30)
        
        choice = input("Выберите действие (0-5): ")
        
        if choice == '1':
            pattern = input("Введите имя, фамилию или телефон для поиска: ")
            results = find_contacts(pattern)
            if results:
                print("\nНайдены совпадения:")
                for r in results:
                    print(f"ID: {r[0]} | {r[1]} {r[2]} | Тел: {r[3]}")
            else:
                print("Ничего не найдено.")
                
        elif choice == '2':
            f_name = input("Имя: ")
            l_name = input("Фамилия: ")
            phone = input("Телефон: ")
            save_contact(f_name, l_name, phone)
            
        elif choice == '3':
            print("Вводите данные контакта. Для завершения введите 'stop' вместо имени.")
            batch = []
            while True:
                f_name = input("Имя (или 'stop'): ")
                if f_name.lower() == 'stop':
                    break
                l_name = input("Фамилия: ")
                phone = input("Телефон: ")
                batch.append((f_name, l_name, phone))
            insert_batch(batch)
            
        elif choice == '4':
            try:
                # Просим пользователя ввести настройки
                # Используем .strip(), чтобы пустой ввод не вызывал ошибку, а ставил значение по умолчанию
                size_input = input("Сколько контактов выводить на странице? (по умолчанию 5): ")
                size = int(size_input) if size_input.strip() else 5
                
                page_input = input("С какой страницы начать? (по умолчанию 1): ")
                page = int(page_input) if page_input.strip() else 1

                while True:
                    print(f"\n--- Страница {page} (размер: {size}) ---")
                    records = get_page(page, size)
                    
                    if not records:
                        print("Записей на этой странице нет.")
                        break
                        
                    for r in records:
                        print(f"ID: {r[0]} | {r[1]} {r[2]} | Тел: {r[3]}")
                    
                    if len(records) < size:
                        print("--- Конец списка ---")
                        break
                        
                    print("\n[Enter] - Дальше | [n] - Перейти на номер страницы | [q] - Выход в меню")
                    nav = input("Выбор: ").lower()
                    
                    if nav == 'q':
                        break
                    elif nav == 'n':
                        page = int(input("Введите номер страницы: "))
                    else:
                        page += 1
            except ValueError:
                print("Ошибка: пожалуйста, вводите только целые числа для размера и номера страницы.")
                
        elif choice == '5':
            print("1 - Удалить по Имени/Фамилии")
            print("2 - Удалить по Телефону")
            del_choice = input("Ваш выбор: ")
            
            if del_choice == '1':
                name_to_del = input("Введите точное имя или фамилию: ")
                remove_contact(name=name_to_del)
            elif del_choice == '2':
                phone_to_del = input("Введите номер телефона: ")
                remove_contact(phone=phone_to_del)
            else:
                print("Неверный выбор.")
                
        elif choice == '0':
            print("Выход из программы. До встречи!")
            break
        else:
            print("Неверная команда. Попробуйте снова.")

# # Список тестовых контактов (30 штук)
# sample_contacts = [
#     ('Иван', 'Иванов', '89001112233'), ('Анна', 'Смирнова', '89112223344'),
#     ('Петр', 'Петров', '89223334455'), ('Елена', 'Кузнецова', '89334445566'),
#     ('Дмитрий', 'Соколов', '89445556677'), ('Мария', 'Попова', '89556667788'),
#     ('Алексей', 'Лебедев', '89667778899'), ('Ольга', 'Козлова', '89778889900'),
#     ('Сергей', 'Новиков', '89889990011'), ('Наталья', 'Морозова', '89990001122'),
#     ('Андрей', 'Петров', '89001234567'), ('Татьяна', 'Волкова', '89112345678'),
#     ('Игорь', 'Соловьев', '89223456789'), ('Светлана', 'Васильева', '89334567890'),
#     ('Артем', 'Зайцев', '89445678901'), ('Виктория', 'Павлова', '89556789012'),
#     ('Михаил', 'Семенов', '89667890123'), ('Ирина', 'Голубева', '89778901234'),
#     ('Максим', 'Виноградов', '89889012345'), ('Юлия', 'Богданова', '89990123456'),
#     ('Николай', 'Воробьев', '89005554433'), ('Оксана', 'Федорова', '89114443322'),
#     ('Антон', 'Беляев', '89223332211'), ('Евгения', 'Тарасова', '89332221100'),
#     ('Роман', 'Белов', '89441110099'), ('Кристина', 'Королева', '89550009988'),
#     ('Валерий', 'Пономарев', '89669998877'), ('Лариса', 'Григорьева', '89778887766'),
#     ('Денис', 'Коновалов', '89887776655'), ('Алла', 'Титова', '89996665544')
# ]

# def seed_database():
#     # Функция для быстрой загрузки тестовых данных
#     print("Начинаю загрузку тестовых контактов...")
#     # Используем твою функцию массовой вставки из phonebook.py
#     insert_batch(sample_contacts)
#     print("Готово! Теперь в базе 30 новых записей.")

# if __name__ == '__main__':
#     seed_database()


if __name__ == '__main__':
    main()