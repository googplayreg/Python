import os
import csv
import json
from connect import get_connection

def export_to_json(file_path="TSIS-es/TSIS1 (Phonebook)/contacts.json"):
    """Экспортирует всех контактов и их телефоны в JSON"""
    conn = get_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            # Получаем контакты и их телефоны (объединяем телефоны в JSON-массив)
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, c.birthday, g.name as group_name,
                       json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.contact_id = p.contact_id
                GROUP BY c.contact_id, g.name;
            """)
            rows = cur.fetchall()
            
            data = []
            for r in rows:
                data.append({
                    "first_name": r[0], "last_name": r[1],
                    "email": r[2], "birthday": str(r[3]) if r[3] else None,
                    "group": r[4], "phones": r[5]
                })
                
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Данные успешно экспортированы в {file_path}")
    finally:
        conn.close()

def import_from_json(file_path="TSIS-es/TSIS1 (Phonebook)/contacts.json"):
    """Импортирует данные из JSON с использованием новой процедуры"""
    if not os.path.exists(file_path):
        print("Файл не найден.")
        return

    conn = get_connection()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with conn.cursor() as cur:
            for item in data:
                # Берем первый телефон из списка, если он есть
                phone_info = item['phones'][0] if item.get('phones') else None
                phone = phone_info['phone'] if phone_info else None
                
                if not phone:
                    continue # Пропускаем, если нет номера

                # Вызываем процедуру upsert (5 параметров)
                cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s)", 
                            (item['first_name'], 
                             item['last_name'], 
                             phone, 
                             item.get('email'), 
                             item.get('birthday')))
                
                # Если в JSON указана группа, перемещаем контакт туда
                if item.get('group'):
                    cur.execute("CALL move_to_group(%s, %s)", (item['first_name'], item['group']))
        
        conn.commit()
        print("Импорт из JSON успешно завершен.")
    except Exception as e:
        print(f"Ошибка при импорте JSON: {e}")
        conn.rollback()
    finally:
        conn.close()

def advanced_view():
    """Интерактивное меню просмотра с пагинацией и сортировкой"""
    page = 1
    size = 5
    sort_by = 'name' # По умолчанию
    group_filter = None

    while True:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Вызываем функцию из БД
                cur.execute("SELECT * FROM get_contacts_advanced(%s, %s, %s, %s)", 
                            (size, (page-1)*size, group_filter, sort_by))
                records = cur.fetchall()

                print(f"\n--- Страница {page} (Сортировка: {sort_by}) ---")
                for r in records:
                    print(f"ID: {r[0]} | {r[1]} {r[2]} | Email: {r[3]} | Группа: {r[5]}")

                print("\nНавигация: [n] След. | [p] Пред. | [s] Сортировка | [f] Фильтр групп | [q] Выход")
                cmd = input(">> ").lower()

                if cmd == 'n': page += 1
                elif cmd == 'p': page = max(1, page - 1)
                elif cmd == 'q': break
                elif cmd == 's':
                    print("1. По имени | 2. По дню рождения | 3. По дате добавления")
                    s_choice = input()
                    sort_by = {'1':'name', '2':'birthday', '3':'date'}.get(s_choice, 'name')
                elif cmd == 'f':
                    group_filter = input("Введите ID группы (или пусто для сброса): ")
                    group_filter = int(group_filter) if group_filter else None
        finally:
            conn.close()

def import_from_csv(file_path):
    """Импортирует данные из CSV с учетом структуры (email, birthday, group)"""
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл {file_path} не найден.")
        return

    conn = get_connection()
    if not conn: return

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            with conn.cursor() as cur:
                for row in reader:
                    # 1. Добавляем/Обновляем основной контакт (UPSERT)
                    cur.execute("""
                        INSERT INTO contacts (first_name, last_name, email, birthday)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (first_name, last_name) 
                        DO UPDATE SET email = EXCLUDED.email, birthday = EXCLUDED.birthday
                        RETURNING contact_id;
                    """, (row['first_name'], row['last_name'], row.get('email'), row.get('birthday') or None))
                    
                    contact_id = cur.fetchone()[0]

                    # 2. Добавляем телефон в связанную таблицу phones
                    if row.get('phone'):
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT DO NOTHING; 
                        """, (contact_id, row['phone'], row.get('type', 'mobile')))

                    # 3. Привязываем к группе (используем нашу процедуру)
                    if row.get('group'):
                        cur.execute("CALL move_to_group(%s, %s)", (row['first_name'], row['group']))

                conn.commit()
                print(f"Импорт из {file_path} успешно завершен!")
    except Exception as e:
        print(f"Ошибка при импорте CSV: {e}")
        conn.rollback()
    finally:
        conn.close()

def main_menu():
    print("\n" + "="*40)
    print("  ADVANCED PHONEBOOK")
    print("="*40)
    print("1. [Просмотр] Постраничный вывод и фильтры")
    print("2. [Поиск] Найти по имени/email/телефону")
    print("3. [Контакт] Добавить/Обновить (UPSERT)")
    print("4. [Группы] Переместить контакт в группу")
    print("5. [Телефоны] Добавить доп. номер")
    print("6. [Импорт/Экспорт] Работа с JSON/CSV")
    print("7. [Удаление] Удалить контакт")
    print("0. Выход")
    print("="*40)

def main():
    # Инициализация таблиц при запуске (код из Этапа 1)
    # create_tables() 

    while True:
        main_menu()
        choice = input("Выберите действие: ").strip()

        if choice == '1':
            advanced_view() # Функция с навигацией [n/p]
        
        elif choice == '2':
            query = input("Введите поисковый запрос: ")
            conn = get_connection()
            with conn.cursor() as cur:
                # Вызываем search_contacts из procedures.sql
                cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                results = cur.fetchall()
                for r in results:
                    print(f"ID: {r[0]} | {r[1]} {r[2]} | Email: {r[3]} | Тел: {r[4]}")
            conn.close()

        elif choice == '3':
            f_name = input("Имя: ")
            l_name = input("Фамилия: ")
            phone = input("Телефон: ")
            email = input("Email (можно пропустить): ")
            birthday = input("День рождения (ГГГГ-ММ-ДД, можно пропустить): ")
            
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s)", 
                            (f_name, l_name, phone, email or None, birthday or None))
                conn.commit()
            print("Контакт успешно сохранен!")
            conn.close()

        elif choice == '4':
            name = input("Имя контакта: ")
            group = input("Название группы: ")
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s)", (name, group))
                conn.commit()
            print(f'Контакт {name}, перемещен (если был), или добавлен в новую группу.')
            conn.close()

        elif choice == '5':
            # Добавление дополнительного номера (реализация 1-ко-многим)
            name = input("Введите имя или фамилию контакта: ")
            new_phone = input("Введите новый номер телефона: ")
            p_type = input("Тип номера (home, work, mobile): ").strip().lower()
            if p_type not in ['home', 'work', 'mobile']:
                p_type = 'mobile' # Значение по умолчанию
            
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s)", (name, new_phone, p_type))
                conn.commit()
            print(f"Дополнительный номер для '{name}' успешно добавлен.")
            conn.close()

        elif choice == '6':
            print("1. Экспорт в JSON | 2. Импорт из JSON | 3. Импорт из CSV")
            sub_choice = input(">> ")
            if sub_choice == '1': export_to_json()
            elif sub_choice == '2': import_from_json()
            elif sub_choice == '3':
                file_name = "TSIS-es/TSIS1 (Phonebook)/contacts.csv"
                import_from_csv(file_name)

        elif choice == '7':
            # Удаление контакта по имени или номеру телефона
            target = input("Введите имя, фамилию или телефон для удаления: ")
            confirm = input(f"Вы уверены, что хотите удалить '{target}'? (y/n): ")
            
            if confirm.lower() == 'y':
                conn = get_connection()
                with conn.cursor() as cur:
                    # Вызываем процедуру удаления
                    cur.execute("CALL delete_contact_adv(%s)", (target,))
                    conn.commit()
                print("Запись (если она существовала) удалена.")
                conn.close()

        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()