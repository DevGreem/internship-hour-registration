from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

class PDFExporter:
    def __init__(self, header_path="header.png", footer_path="footer.png", output_path="reporte_horas.pdf"):
        self.header_path = header_path
        self.footer_path = footer_path
        self.output_path = output_path

    def export(self, data):
        # Configuración del documento
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        style_cell = styles["BodyText"]
        style_cell.fontSize = 9
        
        # 1. HEADER (Solo se agrega si existe la imagen)
        if os.path.exists(self.header_path):
            try:
                # Ajustamos la imagen al ancho de la página (menos márgenes)
                available_width = A4[0] - 4*cm
                img = Image(self.header_path)
                
                # Escalado proporcional si es muy grande
                img_width = img.drawWidth
                img_height = img.drawHeight
                
                if img_width > available_width:
                    factor = available_width / img_width
                    img.drawWidth = available_width
                    img.drawHeight = img_height * factor
                
                elements.append(img)
                elements.append(Spacer(1, 1*cm)) # Espacio entre header y tabla
            except Exception as e:
                print(f"No se pudo cargar el header: {e}")

        # 2. TABLA DE DATOS
        headers = ['Fecha', 'Actividades', 'Tiempo', 'Observaciones']
        table_data = [headers]
        
        for row in data:
            # row: (id, fecha, actividades, tiempo, observaciones)
            fecha_str = row[1]
            
            # Convertir fecha a formato DD-MM-YYYY si está en YYYY-MM-DD
            try:
                # Intentar parsear como YYYY-MM-DD
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha_str = fecha_obj.strftime("%d-%m-%Y")
            except:
                # Si falla, asumir que ya está en el formato correcto
                pass
            
            actividades = Paragraph(row[2], style_cell)
            tiempo = f"{row[3]} h"
            observaciones = Paragraph(row[4], style_cell)
            
            table_data.append([fecha_str, actividades, tiempo, observaciones]) # type: ignore

        # Anchos de columna
        col_widths = [2.5*cm, 8*cm, 2*cm, 4.5*cm]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Estilos de la tabla
        t.setStyle(TableStyle([
            # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), # Eliminado para transparencia
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'), # Encabezados centralizados
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # ('BACKGROUND', (0, 1), (-1, -1), colors.white), 
        ]))
        
        elements.append(t)
        
        # 3. FOOTER (Al final del contenido)
        if os.path.exists(self.footer_path):
            try:
                elements.append(Spacer(1, 1*cm)) # Espacio entre tabla y footer
                
                available_width = A4[0] - 4*cm
                img = Image(self.footer_path)
                
                img_width = img.drawWidth
                img_height = img.drawHeight
                
                if img_width > available_width:
                    factor = available_width / img_width
                    img.drawWidth = available_width
                    img.drawHeight = img_height * factor
                
                elements.append(img)
            except Exception as e:
                print(f"No se pudo cargar el footer: {e}")
        
        # Generar PDF final
        try:
            doc.build(elements)
            print(f"PDF exportado exitosamente a '{self.output_path}'")
        except Exception as e:
            print(f"Error al generar PDF: {e}")
