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
import uuid
import json


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
        if kv_pair.key:            
            kvs[kv_pair.key.content] = kv_pair.value.content if kv_pair.value else ""


    outlog = []
    for page in result.pages:
        outlog.append(f"----Analyzing document from page #{page.page_number}----")
        outlog.append(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        for line_idx, line in enumerate(page.lines):
            words = line.get_words()
            outlog.append(f"...Line # {line_idx} has {len(words)} words and text '{line.content}'")

            for word in words:
                outlog.append(f"......Word '{word.content}' has a confidence of {word.confidence}")

        for selection_mark in page.selection_marks:
            outlog.append(f"...Selection mark is '{selection_mark.state}' and has a confidence of {selection_mark.confidence}")

    for table_idx, table in enumerate(result.tables):
        outlog.append(f"Table # {table_idx} has {table.row_count} rows and {table.column_count} columns")
        for region in table.bounding_regions:
            outlog.append(f"Table # {table_idx} location on page: {region.page_number}")
        for cell in table.cells:
            outlog.append(f"...Cell[{cell.row_index}][{cell.column_index}] has content '{cell.content}'")
            for region in cell.bounding_regions:
                outlog.append(f"...content on page {region.page_number} is within bounding polygon \n")

    outlog.append("----------------------------------------")

    return kvs


def main(collection: str) -> str:
    
    logging.info(str(collection))

    output = analyze_document(collection[0], collection[1])

    return {
        'filepath': collection[0],
        'page': collection[1],
        'output': output
    }