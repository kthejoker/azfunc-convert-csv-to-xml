import logging, tempfile, sys, csv
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
        temp_file_path = tempfile.gettempdir()
        fp = tempfile.NamedTemporaryFile(mode="r+b",suffix=".xml")
       # f = open("temp.xml", "r+b") # temp file for manipulating CSV
        logging.info(fp.name)
    except:
       logging.error("Error opening temp file for reading")
    for row in myfile:
       converted_row = convert_row(row)
       #logging.info('converted_row: %s', converted_row)
       fp.write(bytes(converted_row, 'utf-8'))
       #fp.seek(0,2)
       #logging.info(fp.tell())
    fp.seek(0,0)
    outputxml.set(fp.read())

    return func.HttpResponse(
       "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200
    )
