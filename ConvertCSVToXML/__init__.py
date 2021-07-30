import logging, tempfile, sys, csv
from io import StringIO, BytesIO
import azure.functions as func


def convert_row(row):
    return """<row>
    <borough>%s</borough>
    <classsize>%s</classsize>
    </row>""" % (row["BOROUGH"], row["AVERAGE CLASS SIZE"])

def main(req: func.HttpRequest, inputcsv: func.InputStream, outputxml: func.Out[func.InputStream]) -> func.HttpResponse:
    logging.info("Beginning function")
    inputfile_as_text = StringIO(inputcsv.read().decode("utf-8")) # convert blob to CSV
    logging.info("Read file as string ...")
    try:
        my_csv_reader = csv.DictReader(inputfile_as_text, delimiter=",") #first row as header
    except:
        logging.error("Error opening CSV")

    try:
        temp_file_path = tempfile.gettempdir()
        fp = tempfile.NamedTemporaryFile(mode="r+b",suffix=".xml")
        logging.info(fp.name)
    except:
       logging.error("Error opening temp file for reading")
    for row in my_csv_reader:
       converted_row = convert_row(row)
       fp.write(bytes(converted_row, 'utf-8'))
    fp.seek(0,0)
    outputxml.set(fp.read())

    return func.HttpResponse(
       "XML file created successfully",
        status_code=200
    )
