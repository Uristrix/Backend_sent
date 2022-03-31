import xlsxwriter
import os


def create_xlsx(data):
    num, b_i = sum([len(files) for r, d, files in os.walk("tmp")]), 1

    workbook = xlsxwriter.Workbook('tmp/file{0}.xlsx'.format(str(num + 1)))
    worksheet = workbook.add_worksheet('Data')

    len_phr = len(list(data['data'][0]['sentences'][0].keys())) - 1
    arr = [30, 15, 45] + [30 for _ in range(len_phr)]

    for i, el in enumerate(arr):
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

    header = list(data['data'][0].keys()) + list(data['data'][0]['sentences'][0].keys())[1:]
    for i, el in enumerate(header):
        worksheet.write(0, i, el, style)

    for i, el in enumerate(data['data']):
        for j, el2 in enumerate(el):
            if el2 != 'sentences':
                if len(el['sentences']) != 1:
                    worksheet.merge_range(b_i, j, b_i + len(el['sentences']) - 1, j, ', '.join(el[el2]), style2)
                else:
                    worksheet.write(b_i, j, ', '.join(el[el2]), style2)

        for j, el2 in enumerate(el['sentences']):
            for k, el3 in enumerate(el2, 2):
                worksheet.write(b_i + j, k, ', '.join(el2[el3]), style3)

        b_i += len(el['sentences'])
    workbook.close()
