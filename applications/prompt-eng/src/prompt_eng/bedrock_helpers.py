from typing import Dict, Any
import json
import logging

from botocore.exceptions import ClientError


MODEL_ID = 'amazon.titan-text-express-v1'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ImageError(Exception):
    "Custom exception for errors returned by Titan Text G1 - Express model"

    def __init__(self, message):
        self.message = message


def bedrock_prompt_request(bedrock_client: Any, prompt: str, text_gen_config: Dict[str, Any], model_id: str = 'amazon.titan-text-express-v1'):
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")


        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": text_gen_config
        })

        response_body = __generate_text(bedrock_client, MODEL_ID, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Token count: {result['tokenCount']}")
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")
        
        return result['outputText'] # assuming only one as so far it always return one. Pay attention in case there's logs (prints above) for more than one result

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
                format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)


def __generate_text(bedrock_client: Any, model_id: str, body: Dict[str, Any]):
    logger.info("Generating text with Titan Text G1 - Express model %s", model_id)

    accept = "application/json"
    content_type = "application/json"

    response = bedrock_client.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Titan Text G1 - Express model %s", model_id)

    return response_body
