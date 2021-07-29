import logging
import csv
from io import StringIO, BytesIO
import azure.functions as func


def convert_row(row):
    return """<row>
    <borough>%s></borough>
    <classsize>%s</classsize>
    </row>""" % (row["BOROUGH"], row["AVERAGE CLASS SIZE"])

def main(req: func.HttpRequest, inputcsv: func.InputStream, outputxml: func.Out[func.InputStream]) -> func.HttpResponse:
    logging.info("Beginning function")
    x = StringIO(inputcsv.read().decode("utf-8")) # convert blob to CSV
    logging.info("Read file as string ...")
    try:
        myfile = csv.DictReader(x, delimiter=",") # create reader
    except:
        logging.error("Error opening CSV")

    try:
        f = open("temp.xml", "r+b") # temp file for manipulating CSV
    except:
        logging.error("Error opening temp file for reading")
    for row in myfile:
       converted_row = convert_row(row)
       f.write(bytes(converted_row, 'utf-8'))
    outputxml.set(f.read())

    return func.HttpResponse(
       "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200
    )
