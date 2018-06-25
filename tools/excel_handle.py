import xlwt
from flask import make_response


def save_excel_to_response(excel_header, row_list, sheet_name='1st', filename='download.xls'):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet(sheet_name)

    excel_data = []
    excel_data.extend(row_list[:])
    excel_data.insert(0, excel_header)

    for row,rowdata in enumerate(excel_data):
        for col, val in enumerate(rowdata):
            sheet.write(row, col, val, style=xlwt.Style.default_style)

    response = make_response(book)
    response.headers['content_type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename={filename}'.format(filename=filename)
    return response