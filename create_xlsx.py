import xlsxwriter
import os


def create_xlsx(data):
    num, b_i = sum([len(files) for r, d, files in os.walk("tmp")]), 1

    workbook = xlsxwriter.Workbook('tmp/file{0}.xlsx'.format(str(num)))
    worksheet = workbook.add_worksheet('Data')
    for i, el in enumerate([30, 15, 45, 30, 30, 30]):
        worksheet.set_column(i, i, el)

    style = workbook.add_format({
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '00AEFF',
        "font_color": "white"
    })

    style2 = workbook.add_format({
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': 'F0FFFF',
        'text_wrap': 1
    })

    style3 = workbook.add_format({
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': 'D2D2D2',
        'text_wrap': 1
    })

    header = list(data['data'][0].keys())[:-1] + list(data['data'][0]['sentences'][0].keys())

    for i, el in enumerate(header):
        worksheet.write(0, i, el, style)

    for i, el in enumerate(data['data']):
        worksheet.merge_range(b_i, 0, b_i + len(el['sentences']) - 1, 0, ', '.join(el['key phrases']), style2)
        worksheet.merge_range(b_i, 1, b_i + len(el['sentences']) - 1, 1, el['paragraph num'], style2)

        for j, el2 in enumerate(el['sentences']):
            worksheet.write(b_i + j, 2, el2['text'], style3)
            worksheet.write(b_i + j, 3, ', '.join(el2['date/time']), style3)
            worksheet.write(b_i + j, 4, ', '.join(el2['rest entities']), style3)
            worksheet.write(b_i + j, 5, ', '.join(el2['keywords']), style3)

        b_i += len(el['sentences'])
    workbook.close()
