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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT UNIQUE
            )
        """)
        self.conn.commit()
        self._migrate_activities()

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

    def _migrate_activities(self):
        """Migrar actividades únicas de registros a activities"""
        self.cursor.execute("SELECT DISTINCT actividades FROM registros WHERE actividades != ''")
        existing_activities = self.cursor.fetchall()
        for (activity,) in existing_activities:
            try:
                self.cursor.execute("INSERT OR IGNORE INTO activities (description) VALUES (?)", (activity,))
            except:
                pass
        self.conn.commit()

    def get_all_activities(self):
        """Obtener todas las actividades ordenadas alfabéticamente"""
        self.cursor.execute("SELECT description FROM activities ORDER BY description")
        return [row[0] for row in self.cursor.fetchall()]

    def add_activity(self, description):
        """Agregar una nueva actividad si no existe"""
        try:
            self.cursor.execute("INSERT OR IGNORE INTO activities (description) VALUES (?)", (description,))
            self.conn.commit()
        except:
            pass

    def update_record(self, record_id, field, value):
        """Actualizar un campo específico de un registro"""
        if field in ['actividades', 'observaciones', 'fecha', 'tiempo']:
            self.cursor.execute(f"UPDATE registros SET {field} = ? WHERE id = ?", (value, record_id))
            self.conn.commit()
            return True
        return False

    def get_record_by_id(self, record_id):
        """Obtener un registro por su ID"""
        self.cursor.execute("SELECT * FROM registros WHERE id = ?", (record_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
