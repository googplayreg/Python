import os
import csv
import json
from connect import get_connection

def get_available_groups():
    """Возвращает список имен существующих групп"""
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM groups ORDER BY name;")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()

def show_groups_ui():
    """Печатает список групп в удобном виде"""
    groups = get_available_groups()
    if groups:
        print("\nСуществующие группы:", ", ".join(groups))
    else:
        print("\nГрупп пока нет. Вы можете создать новую, введя любое название.")

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
    page = 1
    size = 5
    sort_by = 'name'
    group_filter = None

    while True:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_advanced(%s, %s, %s, %s)", 
                            (size, (page-1)*size, group_filter, sort_by))
                records = cur.fetchall()

                print(f"\n--- Страница {page} | Фильтр: {group_filter or 'Все'} | Сортировка: {sort_by} ---")
                if not records:
                    print("Записей нет.")
                for r in records:
                    print(f"ID: {r[0]} | {r[1]} {r[2]} | Email: {r[3]} | Группа: {r[5]}")

                print("\n[n] Вперед | [p] Назад | [s] Сортировка | [f] Фильтр групп | [c] Сброс фильтра | [q] Выход")
                cmd = input(">> ").lower()

                if cmd == 'n': page += 1
                elif cmd == 'p': page = max(1, page - 1)
                elif cmd == 'q': break
                elif cmd == 'c': group_filter = None
                elif cmd == 's':
                    print("1. Имя | 2. День рождения | 3. Дата добавления")
                    s_choice = input(">> ")
                    sort_by = {'1':'name', '2':'birthday', '3':'date'}.get(s_choice, 'name')
                elif cmd == 'f':
                    show_groups_ui()
                    group_filter = input("Введите название группы для фильтрации: ").strip()
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
    print("5. [Телефоны] Добавить дополнительный номер")
    print("6. [Импорт/Экспорт] Работа с JSON/CSV")
    print("7. [Удаление] Удалить контакт")
    print("0. Выход")
    print("="*40)

def main():
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
            email = input("Email: ")
            bday = input("День рождения (ГГГГ-ММ-ДД) или пусто: ")
            
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("CALL upsert_full_contact(%s, %s, %s, %s, %s)", 
                            (f_name, l_name, phone, email or None, bday or None))
                conn.commit()
            print(f"Данные контакта '{f_name} {l_name}' успешно обновлены/добавлены.")
            conn.close()

        elif choice == '4':
            f_name = input("Имя контакта: ")
            l_name = input("Фамилия контакта: ")
            show_groups_ui()
            group_name = input("Введите название группы: ").strip()
            
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s, %s)", (f_name, l_name, group_name))
                conn.commit()
            print("Готово!")
            conn.close()

        elif choice == '5':
            f_name = input("Имя контакта: ")
            l_name = input("Фамилия контакта: ")
            new_phone = input("Новый номер: ")
            p_type = input("Тип (mobile/work/home): ")
            
            conn = get_connection()
            with conn.cursor() as cur:
                # Находим ID по имени и фамилии
                cur.execute("SELECT contact_id FROM contacts WHERE first_name=%s AND last_name=%s", (f_name, l_name))
                res = cur.fetchone()
                if res:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                                (res[0], new_phone, p_type or 'mobile'))
                    conn.commit()
                    print("Номер добавлен.")
                else:
                    print("Контакт не найден.")
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
            f_name = input("Имя для удаления: ")
            l_name = input("Фамилия для удаления: ")
            confirm = input(f"Вы уверены что хотите удалить {f_name} {l_name}? (y/n): ")
            if confirm.lower() == 'y':
                conn = get_connection()
                with conn.cursor() as cur:
                    cur.execute("CALL delete_contact_safe(%s, %s)", (f_name, l_name))
                    conn.commit()
                print("Запись удалена.")
                conn.close()

        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()