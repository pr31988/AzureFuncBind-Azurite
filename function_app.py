import azure.functions as func
import logging
import csv
import codecs

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.function_name('secondHttpFunction')
@app.route(route="newRoute")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        "Hey! that second function also worked!!!",
        status_code=200
    )


# blob trigger function; triggered on people.csv file upload and read the content
@app.function_name("blobFuncTrigger")
@app.blob_trigger(
    arg_name="myblob",
    path="newcontainer/people.csv",
    connection="AzureWebJobsStorage"   # To run function with data storage locally (using Azurite & Azure storage explorer) 
)
@app.blob_output(      # output binding to create a copy of input file
    arg_name="OutBlob",
    path="processed/people1.csv",    
    connection="AzureWebJobsStorage"
)

def test_function(myblob: func.InputStream, OutBlob: func.Out[str]):

    logging.info(
        f"Blob trigger fired.\n"
        f"Blob name: {myblob.name}\n"
        f"Blob size: {myblob.length} bytes"
    )

    # decode the input stream and read it as csv
    reader = csv.reader(
                        codecs.iterdecode(myblob,'UTF-8')
                    )

    output_lines = []
    for row in reader:
        logging.info(row)
        output_lines.append(','.join(row))

    # write to output file
    OutBlob.set("\n" .join(output_lines))
 
