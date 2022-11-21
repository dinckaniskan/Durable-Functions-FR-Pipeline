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


def analyze_layout(filepath):

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    blob_client = BlobClient.from_blob_url(f"{filepath}?{sas_token}")
    file_handle = blob_client.download_blob()

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", document=file_handle
    )

    result = poller.result()


    cert_pages = []

    for page in result.pages:

        for line_idx, line in enumerate(page.lines):

            if line.content.lower().__contains__('phytosanitary certificate'):
                cert_pages.append(page.page_number)
            else:
                words = line.get_words()

                found_phytosanitary = False
                found_certificate = False

                for word in words:
                    if word.content.lower().__contains__('phytosanitary'):
                        found_phytosanitary = True
                    if word.content.lower().__contains__('certificate'):
                        found_certificate = True

                if found_phytosanitary and found_certificate:
                    cert_pages.append(page.page_number)

        cert_pages = list(set(cert_pages))

    return cert_pages


def main(filepath: str) -> str:
    cert_pages = analyze_layout(filepath)

    return filepath, cert_pages
