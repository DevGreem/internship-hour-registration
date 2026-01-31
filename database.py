import sqlite3

class Database:
    def __init__(self, db_name="internship_logs.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                actividades TEXT,
                tiempo REAL,
                observaciones TEXT
            )
        """)
        self.conn.commit()

    def add_record(self, fecha, actividades, tiempo, observaciones):
        self.cursor.execute("""
            INSERT INTO registros (fecha, actividades, tiempo, observaciones)
            VALUES (?, ?, ?, ?)
        """, (fecha, actividades, tiempo, observaciones))
        self.conn.commit()
        print("Registro agregado exitosamente.")

    def get_all_records(self):
        # Ordenar por fecha convirtiendo DD-MM-YYYY a formato comparable
        # substr(fecha, 7, 4) = año, substr(fecha, 4, 2) = mes, substr(fecha, 1, 2) = día
        self.cursor.execute("""
            SELECT * FROM registros 
            ORDER BY 
                CASE 
                    WHEN fecha LIKE '__-__-____' THEN substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
                    ELSE fecha 
                END
        """)
        return self.cursor.fetchall()

    def get_total_hours(self):
        self.cursor.execute("SELECT SUM(tiempo) FROM registros")
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def close(self):
        self.conn.close()
