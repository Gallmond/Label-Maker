import csv, datetime
from xhtml2pdf import pisa

# globals
nowDatetime = datetime.datetime.now()
nowString = nowDatetime.strftime("%Y-%m-%d %H:%M:%S"); # yyyy-mm-dd hh:mm:ss
reportInfo = {
	"csvlines":0,
	"successes":0,
	"failures":0,
	"errorLines":[]
}

# utility functions
def errorCollector(_errorString):
	reportInfo["failures"] += 1
	reportInfo["errorLines"].append(_errorString)

def reportWriter():
	errorLines = ""
	for errorLineEntry in reportInfo["errorLines"]:
		errorLines+= errorLineEntry+"\n"

	reportString = (
		"==== %s ====\n" # nowString
		"> csv loaded with %s rows\n" # reportInfo["csvlines"]
		"> successfully processed %s rows\n" # reportInfo["successes"]
		"> failed to process %s rows with errors:\n" # reportInfo["failures"]
		"%s" # errorLines
		%
		(nowString, reportInfo["csvlines"], reportInfo["successes"],  reportInfo["failures"], errorLines)
		)

	try:
		with open("report.txt", "a") as reportFile:
			reportFile.write(reportString)
		print("wrote to report.txt")
	except:
		print("Error creating report.txt")

def convertHtmlToPdf(sourceHtml, outputFilename):
	# open output file for writing (truncated binary)
	resultFile = open(outputFilename, "w+b")
	# convert HTML to PDF
	pisaStatus = pisa.CreatePDF(
			sourceHtml,                # the HTML to convert
			dest=resultFile)           # file handle to recieve result
	# close output file
	resultFile.close()                 # close output file
	# return True on success and False on errors
	return pisaStatus.err

def mainFunction():
	# read rows from CSV file
	rowsToProcess = []
	with open('input/barcodes.csv', newline='') as csvFile:
		reader = csv.reader(csvFile)
		for row in reader:
			rowsToProcess.append(row)
			# print(row)

	print("csv has",len(rowsToProcess),"rows");
	reportInfo["csvlines"] = len(rowsToProcess)

	exelIndex = 0;
	for row in rowsToProcess:
		exelIndex+=1
		# attempt to select row data
		try:
			barcodeNumStr = row[0]
			barcodeNumInt = float(barcodeNumStr)
			pNumber = row[1]
			pNumberStr = pNumber.replace("/","") # for filenames. P180351B-M/XL becomes P180351B-MXL
			description = row[2]
			colour = row[3]
		except ValueError:
			print("ValueError trying to parse row", row)
			errorCollector( "row %s: ValueError trying to parse row: %s" % (exelIndex, row) )
			continue;
		except:
			print("Unknown error trying to parse row", row)
			errorCollector( "row %s: Unknown error trying to parse row: %s" % (exelIndex, row) )
			continue;

		try:
			with open('label_template.html', 'r') as myfile:
				thisBarcodeHTML = myfile.read();
		except:
			print("Error reading label_template")
			errorCollector( "row %s: Error reading label_template" % (exelIndex) )
			continue

		# replace placeholders
		thisBarcodeHTML = thisBarcodeHTML.replace("P_NUMBER_VALUE_HERE", pNumber)
		thisBarcodeHTML = thisBarcodeHTML.replace("COLOUR_VALUE_HERE", colour)
		thisBarcodeHTML = thisBarcodeHTML.replace("DESCRIPTION_VALUE_HERE", description[:40]) # description clipped to first 40 characters
		thisBarcodeHTML = thisBarcodeHTML.replace("BARCODE_VALUE_HERE", barcodeNumStr)
		outputFilename = "output/"+pNumberStr+".pdf"

		try:
			pisa.showLogging()
			convertHtmlToPdf(thisBarcodeHTML, outputFilename)
			reportInfo["successes"] +=1
		except:
			print("error creating pdf", outputFilename)
			errorCollector( "row %s: Error creading pdf %s" % (exelIndex, outputFilename) )
			continue
		
		print("created", outputFilename)

	reportWriter()
	print("finished with", reportInfo["successes"], "files created and", reportInfo["failures"], "errors. See report.txt for info")
	input("Press enter to finish...")

# run main
if __name__ == "__main__":
	try:
		mainFunction()
	except SystemExit as e:
		print('Error!', e)
		print('Press enter to exit')
		raw_input()
