from openpyxl import Workbook
from datetime import date


def writeToExcel(members, listNr):
	wb = Workbook()

	ws = wb.active

	ws.append(['Huisgenoot', 'Turfjes'])

	for member in members:
		ws.append([member[0], member[1]])

	filename = str(listNr) + '-'
	filename += date.today().isoformat()
	filename += '.xlsx'

	wb.save('../data/sheets/' + filename)

	return filename