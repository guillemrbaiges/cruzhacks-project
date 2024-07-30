from typing import Dict, Any, Tuple
import json
import logging
import boto3
import textwrap
from botocore.exceptions import ClientError

from prompt_eng.bedrock_helpers import bedrock_prompt_request
from prompt_eng.prompts import extract_defended_position, extract_speech_quality_report, prettify_to_markdown

BEDROCK_SERVICE = 'bedrock-runtime'
REGION = 'eu-central-1'


def get_speech_quality_report(input_text: str, text_gen_config: Dict[str, Any]) -> Tuple[str, str]:

    bedrock_client = boto3.client(service_name=BEDROCK_SERVICE, region_name=REGION)

    defended_position = bedrock_prompt_request(
        bedrock_client,
        extract_defended_position(input_text),
        text_gen_config
    )

    speech_quality_report = bedrock_prompt_request(
        bedrock_client, 
        extract_speech_quality_report(
            input_text,
            defended_position
        ), 
        text_gen_config
    )

    '''markdown_report = bedrock_prompt_request(
        bedrock_client, 
        prettify_to_markdown(speech_quality_report), 
        text_gen_config
    )'''

    speech_quality_report = speech_quality_report.replace("\n    ", "\n")

    print("Defended position:", defended_position, "\n\n")
    print("Final Speech Quality Report:", speech_quality_report)

    return defended_position, speech_quality_report
