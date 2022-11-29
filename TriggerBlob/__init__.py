import logging
import uuid
import json
import os

import azure.functions as func
import azure.durable_functions as df


async def main(myblob: func.InputStream, starter: str, execution: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    sas_token = os.getenv("SasToken")

    client = df.DurableOrchestrationClient(starter)
    
    logging.info(f"{myblob.uri}")

    content = {
        'docs': [
            f"{myblob.uri}",
        ]
    }
    logging.info("----------------------")    
    logging.info(content)
    logging.info("----------------------")    

    instance_id = await client.start_new("ExtractCertificate", None, content)    

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    rowKey = str(uuid.uuid4())
    
    logging.info(f"rowKey = '{rowKey}'.")

    check_status_response = client.get_client_response_links(None, instance_id)
    logging.info(f"check_status_response = {check_status_response}")
    
    execution_message = {
        "Name": "Output binding message",
        "PartitionKey": "execution",
        "RowKey": rowKey,
        "Input": "BlobTrigger",
        "BlobReference": myblob.uri,
        "ExecutionLinks": check_status_response
    }

    execution_message_text = json.dumps(execution_message)    

    execution.set(val=execution_message_text)
    