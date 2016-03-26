from openpyxl import Workbook
from datetime import date
import os


def writeToExcel(members, l):
    wb = Workbook()

    ws = wb.active

    ws.append(['Huisgenoot', 'Turfjes'])

    for member in members:
        ws.append([member[0], member[1]])

    listDate = l.date.date().isoformat()

    filename = '{}-{}.xlsx'.format(l.id, listDate)

    basepath = os.path.dirname(__file__)
    f = os.path.abspath(os.path.join(basepath, os.pardir, 
        'data/sheets/{}'.format(filename)))

    wb.save(f)

    return filename