# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobClient


endpoint = os.getenv("FormRecognizerEndpoint")
key = os.getenv("FormRecognizerKey")
sas_token = os.getenv("SasToken")


def analyze_document(filepath, page):

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    blob_client = BlobClient.from_blob_url(f'{filepath}?{sas_token}')
    file_handle = blob_client.download_blob()

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", document=file_handle, pages=page
    )

    result = poller.result()

    kvs = {}
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            kvs[kv_pair.key.content] = kv_pair.value.content

    return kvs


def main(collection: str) -> str:
    
    logging.info(str(collection))

    output = analyze_document(collection[0], collection[1])

    return {
        'filepath': collection[0],
        'page': collection[1],
        'output': output
    }