"""
Export functionality for the Inventory Management System.
"""
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime


class InventoryExporter:
    """Handles export of inventory data to different formats."""

    @staticmethod
    def to_excel(products, filename=None) -> BytesIO:
        """
        Export inventory data to Excel format.
        
        Args:
            products (List[Dict]): List of product dictionaries
            filename (str, optional): Output filename
            
        Returns:
            BytesIO: Excel file data
        """
        df = pd.DataFrame(products)
        output = BytesIO()
        
        # Create Excel writer with styling
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Inventory', index=False)
            
            # Get the worksheet to apply styling
            worksheet = writer.sheets['Inventory']
            
            # Style the header
            for col in range(len(df.columns)):
                cell = worksheet.cell(row=1, column=col+1)
                cell.font = cell.font.copy(bold=True)
                cell.fill = cell.fill.copy(fgColor="E91E63")  # Magenta theme
                
            # Adjust column widths
            for col in worksheet.columns:
                max_length = 0
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                worksheet.column_dimensions[col[0].column_letter].width = max_length + 2
        
        output.seek(0)
        return output

    @staticmethod
    def to_pdf(products, filename=None) -> BytesIO:
        """
        Export inventory data to PDF format with custom branding.
        
        Args:
            products (List[Dict]): List of product dictionaries
            filename (str, optional): Output filename
            
        Returns:
            BytesIO: PDF file data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#E91E63'),  # Magenta theme
            spaceAfter=30
        )
        
        # Title with timestamp
        title = Paragraph(
            f"Inventory Report<br/><font size=12>{datetime.now().strftime('%Y-%m-%d %H:%M')}</font>",
            title_style
        )
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Convert data to table format
        if products:
            data = [list(products[0].keys())]  # Headers
            for product in products:
                data.append([str(value) for value in product.values()])
            
            # Create and style the table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E91E63')),  # Header background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
                ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Content background
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Content text
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Content font
                ('FONTSIZE', (0, 1), (-1, -1), 10),  # Content font size
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
            ]))
            elements.append(table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
