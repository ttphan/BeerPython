from openpyxl import Workbook
from datetime import date


def writeToExcel(members, l):
	wb = Workbook()

	ws = wb.active

	ws.append(['Huisgenoot', 'Turfjes'])

	for member in members:
		ws.append([member[0], member[1]])

	listDate = l.date.date().isoformat()

	filename = '{}-{}.xlsx'.format(l.id, listDate)

	wb.save('../data/sheets/' + filename)

	return filename