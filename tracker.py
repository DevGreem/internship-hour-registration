from datetime import datetime
from database import Database
from exporter import PDFExporter

def main():
    db = Database()
    # Ahora buscamos imágenes, no un PDF plantilla
    header_file = "header.png"
    footer_file = "footer.png"
    
    exporter = PDFExporter(header_path=header_file, footer_path=footer_file)

    while True:
        print("\n--- Registro de Horas de Pasantía ---")
        print("1. Agregar registro")
        print("2. Ver registros")
        print("3. Exportar a PDF")
        print("4. Ver total de horas")
        print("5. Salir")
        
        choice = input("Seleccione una opción: ")

        if choice == '1':
            fecha = input("Fecha (DD-MM-YYYY): ")
            if not fecha:
                fecha = datetime.now().strftime("%d-%m-%Y")
            
            actividades = input("Actividades realizadas: ")
            
            while True:
                try:
                    tiempo = float(input("Tiempo de realización (horas): "))
                    break
                except ValueError:
                    print("Por favor ingrese un número válido.")
            
            observaciones = input("Observaciones: ")
            
            db.add_record(fecha, actividades, tiempo, observaciones)

        elif choice == '2':
            records = db.get_all_records()
            print("\n--- Registros Guardados ---")
            print(f"{'ID':<4} | {'Fecha':<12} | {'Tiempo':<6} | {'Actividades':<30} | {'Observaciones'}")
            print("-" * 80)
            for row in records:
                act_display = (row[2][:27] + '...') if len(row[2]) > 27 else row[2]
                obs_display = (row[4][:20] + '...') if len(row[4]) > 20 else row[4]
                print(f"{row[0]:<4} | {row[1]:<12} | {row[3]:<6} | {act_display:<30} | {obs_display}")

        elif choice == '3':
            records = db.get_all_records()
            if not records:
                print("No hay registros para exportar.")
            else:
                exporter.export(records)

        elif choice == '4':
            total = db.get_total_hours()
            print(f"\nTotal de horas registradas: {total} horas")

        elif choice == '5':
            print("Saliendo...")
            db.close()
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
