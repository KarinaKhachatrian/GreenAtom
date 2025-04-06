import time
import psycopg2
import subprocess

db_settings = {
    'dbname': 'flydb',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db'
}

for i in range(10):
    try:
        print(f"Попытка подключения к БД ({i+1}/10)...")
        conn = psycopg2.connect(**db_settings)
        conn.close()
        print("База данных успешно подключена.")
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    print("База данных не доступна.")
    exit(1)

print("Запуск db_manager.py")
subprocess.run(["python", "db_manager.py"], check=True)

print("Запуск flights_report.py")
subprocess.run(["python", "flights_report.py"], check=True)

print("Запуск Streamlit")
subprocess.run(["streamlit", "run", "dashboard.py"])
