from openpyxl import Workbook
from datetime import date


def writeToExcel(dict, listNr):
	wb = Workbook()

	ws = wb.active

	ws.append(['Huisgenoot', 'Turfjes'])

	for key, value in dict.items():
		ws.append([key, value])

	filename = str(listNr) + '-'
	filename += date.today().isoformat()
	filename += '.xlsx'

	wb.save('../data/sheets/' + filename)

	return filename