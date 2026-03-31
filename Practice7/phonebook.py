from connect import get_connection
import csv

def create_phonebook_table():
    # Данная функция создает таблицу contacts (если она ещё не существует)

    # Получаем соединение через наш ранее созданный файл (connect.py)
    conn = get_connection()

    if conn is not None:
        try:
            with conn.cursor() as cur:
                # SQL-запрос для создания таблицы
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contacts (
                        contact_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50),
                        phone_number VARCHAR(20) UNIQUE NOT NULL
                    );
                """)
                # Фиксируем изменения
                conn.commit()
                print('Таблица "contacts" готова к работе.')
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            conn.close()

def insert_from_csv(file_path):
    # Данная функция читает данные из CSV и записывает их в таблицу contacts.
    
    conn = get_connection()
    if conn is None:
        return

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            # Используем DictReader, чтобы обращаться к столбцам по именам
            reader = csv.DictReader(f)

            with conn.cursor() as cur:
                for row in reader:
                    # SQL-запрос с "%s" для безопасности
                    sql = """
                        INSERT INTO contacts (first_name, last_name, phone_number)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (phone_number) DO NOTHING;
                    """
                    # Передаем данные в кортеже
                    values = (row['first_name'], row['last_name'], row['phone_number'])
                    cur.execute(sql, values)

                conn.commit()
                print(f"Данные из {file_path} успешно загружены.")

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")
    finally:
        conn.close()

def add_contact_from_console():
    # Данная функция запрашивает данные у пользователя и добавляет новый контакт
    print("\n--- Добавление нового контакта ---")

    # Ввод данных через консоль
    first_name = input("Введите имя: ").strip()
    last_name = input("Введите фамилию: ").strip()
    phone_number = input("Введите номер телефона: ").strip()

    # Проверка на недопустимые значения
    if not first_name or not phone_number:
        print("Ошибка: Имя и номер телефона обязательны для заполнения!")
        return

    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO contacts (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone_number) DO NOTHING;
                """
                cur.execute(sql, (first_name, last_name, phone_number))
                conn.commit()

                # Проверяем, добавилась ли строка (rowcount покажет 1, если добавлена)
                if cur.rowcount > 0:
                    print(f"Контакт {first_name} успешно добавлен!")
                else:
                    print("Контакт не добавлен (возможно, такой номер уже существует).")

        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
        finally:
            conn.close()

def update_contact():
    # Данная функция обновляет данные контакта

    print("\n---Редактирование контакта---")
    target_phone = input("Введите текущий номер телефона контакта: ").strip()

    print("Что вы хотите изменить?")
    print("1. Имя")
    print("2. Номер телефона")
    choice = input("Выберите вариант (1 или 2): ").strip()

    if choice == '1':
        new_name = input("Введите новое имя: ").strip()
        sql = "UPDATE contacts SET first_name = %s WHERE phone_number = %s;"
        params = (new_name, target_phone)
    elif choice == '2':
        new_phone = input("Введите новый номер телефона: ").strip()
        sql = "UPDATE contacts SET phone_number = %s WHERE phone_number = %s;"
        params = (new_phone, target_phone)
    else:
        print("Некорректный выбор.")
        return

    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()

                if cur.rowcount > 0:
                    print("Данные успешно обновлены!")
                else:
                    print("Контакт с таким номером не найден.")
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")
        finally:
            conn.close()

def search_contacts():
    # Функция для поиска контактов по фильтрам: имя или префикс номера.

    print("\n--- Поиск контактов ---")
    print("1. Найти по имени (или началу имени)")
    print("2. Найти по префиксу номера телефона")
    choice = input("Выберите вариант (1 или 2): ").strip()

    if choice == '1':
        search_term = input("Введите имя (или начало имени): ").strip()
        # ILIKE делает поиск нечувствительным к регистру (Ivan = ivan)
        sql = "SELECT * FROM contacts WHERE first_name ILIKE %s;"
        params = (search_term + '%',) # Добавляем % в конец для поиска "начинается с..."
    elif choice == '2':
        prefix = input("Введите начало номера: ").strip()
        sql = "SELECT * FROM contacts WHERE phone_number LIKE %s;"
        params = (prefix + '%',)
    else:
        print("Некорректный выбор.")
        return

    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                # fetchall() забирает все найденные строки из базы
                results = cur.fetchall()

                if results:
                    print(f"\nНайдено совпадений: {len(results)}")
                    print("-" * 40)
                    for row in results:
                        # row[0] - id, row[1] - имя, row[2] - фамилия, row[3] - телефон
                        print(f"ID: {row[0]} | {row[1]} {row[2] or ''} | Тел: {row[3]}")
                    print("-" * 40)
                else:
                    print("Ничего не найдено.")
        except Exception as e:
            print(f"Ошибка при поиске: {e}")
        finally:
            conn.close()

def delete_contact():
    # Функция для удаления контакта по имени или номеру телефона.

    print("\n--- Удаление контакта ---")
    print("1. Удалить по имени (ВНИМАНИЕ: удалит ВСЕХ с таким именем!)")
    print("2. Удалить по номеру телефона")
    choice = input("Выберите вариант (1 или 2): ").strip()

    if choice == '1':
        name = input("Введите имя для удаления: ").strip()
        sql = "DELETE FROM contacts WHERE first_name = %s;"
        params = (name,)
    elif choice == '2':
        phone = input("Введите номер для удаления: ").strip()
        sql = "DELETE FROM contacts WHERE phone_number = %s;"
        params = (phone,)
    else:
        print("Некорректный выбор.")
        return

    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
                
                # Сообщаем результат
                if cur.rowcount > 0:
                    print(f"Успешное удаление! Удалено записей: {cur.rowcount}.")
                else:
                    print("Ошибка удаления: Контакт не найден")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
        finally:
            conn.close()




def main_menu():
    # Главный цикл программы с выбором действий.
    create_phonebook_table() # Проверяем таблицу при старте
    
    while True:
        print("\n===== ТЕЛЕФОННАЯ КНИГА =====")
        print("1. Загрузить контакты из CSV")
        print("2. Добавить контакт вручную")
        print("3. Редактировать контакт")
        print("4. Поиск контактов")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            insert_from_csv('contacts.csv')
        elif choice == '2':
            add_contact_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main_menu()