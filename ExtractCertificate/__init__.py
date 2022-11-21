import logging
import json

import azure.functions as func
import azure.durable_functions as df
import json


def orchestrator_function(context: df.DurableOrchestrationContext):

    input_data = context.get_input()
    logging.info(f"Received Input {input_data}")

    
    ##########
    parallel_identify_certificate = [ context.call_activity("ActivityIdentifyCertificate", doc) for doc in input_data['docs'] ]
    output_identify_certificate = yield context.task_all(parallel_identify_certificate)

    logging.info(output_identify_certificate)
    ##########


    ##########
    parallel_extract_certificate_tasks = []
    for item in output_identify_certificate:
        for page in item[1]:
            parallel_extract_certificate_tasks.append(context.call_activity("ActivityExtractCertificate", [item[0], page]))
    
    output_extract_certificate = yield context.task_all(parallel_extract_certificate_tasks)
    
    logging.info(output_extract_certificate)
    ##########
            
    return output_extract_certificate


main = df.Orchestrator.create(orchestrator_function)