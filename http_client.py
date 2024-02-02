import requests
import configparser
import json
import threading
import re

config = configparser.ConfigParser()
config.read('config.ini')
url = config.get('OPENAI_API', 'OPENAI_URL')
openai_key = config.get('OPENAI_API', 'OPENAI_API_KEY')


class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, input=None):
        json_data = {
            "messages": [
                {
                    "role": "system",
                    "content": """You are a tibco assistant, you will be given one or more xml codes for activities in tibco. You should explain 
                    the given code in english. Explain the configuration, parameters defined in it, and if there are any key value pairs of the configuration used within this 
                    activities extract them. 

                    Following rules should be ensured when output is generated if not satisfied regenerate the output.
                    Rules:
                    1) Don't just explain the tags present in the code, rather explain the configurations defined int it.
                    2) While producing the output refer to the tibco documentation related to Activities, Flows, Global variables and don't miss the configuration details.
                    3) Don't miss the links,parameter types or parameters or any important tibco configuration details in the output.
                    4) Make sure the activity name, it's type and resourceType is present in the output if those detials are given in the input.
                    5) Make sure that all the QueryOutputCachedSchemaColumns are captured with their QueryOutputCachedSchemaDataTypes and QueryOutputCachedSchemaStatus details. QueryOutputCachedSchemaDataTypes defines the value assigned to the QueryOutputCachedSchemaColumns and QueryOutputCachedSchemaStatus defines if the mapping of the column is required or not.
                    6) If there are any paths in the input binding blocks make sure you mention them in the output. for reference consider below example. The path \"$Start/pfx4:DisbursementRequest/pfx4:caseId\ should be mentioned in the output.
                    <pfx4:caseId>\n
                    <xsl:value-of select=\"$Start/pfx4:DisbursementRequest/pfx4:caseId\"/>\n
                    </pfx4:caseId>\n 
                    5) Once the explanation is done don't summarize again the whole explanation.
                    6) Following is the example for an output. Input is what you will be provided output is what I am expecting you to generate.
                    Input:
                    <pd:activity name=\"InvokeService\">\n<pd:type>com.tibco.plugin.soap.SOAPSendReceiveActivity</pd:type>\n<pd:resourceType>ae.activities.SOAPSendReceiveUI</pd:resourceType>\n<pd:x>452</pd:x>\n<pd:y>92</pd:y>\n<config>\n<timeout>0</timeout>\n<soapAttachmentStyle>SwA</soapAttachmentStyle>\n<timeoutType>Seconds</timeoutType>\n<service>pfx3:CalculationsService</service>\n<servicePort>CalculationsEndpoint1</servicePort>\n<operation>GetDisbursementAmounts</operation>\n<soapAction>/Services/CalculationsService.serviceagent/CalculationsEndpoint1/GetDisbursementAmounts</soapAction>\n<endpointURL>%%Connection/WebService/CalculationServiceURL%%</endpointURL>\n<authScheme>NONE</authScheme>\n</config>\n<pd:inputBindings>\n<inputMessage>\n<pfx4:DisbursementRequest>\n<pfx4:caseId>\n<xsl:value-of select=\"$Start/pfx4:DisbursementRequest/pfx4:caseId\"/>\n</pfx4:caseId>\n<pfx4:applicationNumber>\n<xsl:value-of select=\"if (string-length($Start/pfx4:DisbursementRequest/pfx4:applicationNumber) = 0) then\n\t$GetApplicationNumber/resultSet/Record[1]/APLN_NBR\nelse\n\t$Start/pfx4:DisbursementRequest/pfx4:applicationNumber\"/>\n</pfx4:applicationNumber>\n<pfx4:userId>\n<xsl:value-of select=\"$Start/pfx4:DisbursementRequest/pfx4:userId\"/>\n</pfx4:userId>\n<pfx4:sender>\n<xsl:value-of select=\"$Start/pfx4:DisbursementRequest/pfx4:sender\"/>\n</pfx4:sender>\n<pfx4:autosave>\n<xsl:value-of select='\"true\"'/>\n</pfx4:autosave>\n</pfx4:DisbursementRequest>\n</inputMessage>\n</pd:inputBindings>\n</pd:activity>"

                    output:
                    The given code represents an InvokeService activity in Tibco. The InvokeService activity is used to invoke a SOAP web service. It allows you to configure various parameters and input bindings for the SOAP request. This activity is of type com.tibco.plugin.soap.SOAPSendReceiveActivity. This activity’s resourceType is ae.activities.SOAPSendReceiveUI.The configuration for the InvokeService activity is as follows: timeout: Specifies the timeout value for the SOAP request. In this case, the timeout is set to 0 seconds. soapAttachmentStyle: Specifies the attachment style for the SOAP request. In this case, the attachment style is set to \"SwA\" (SOAP with Attachments). timeoutType: Specifies the unit of the timeout value. In this case, the timeout type is set to \"Seconds\". service: Specifies the service name for the SOAP request. In this case, the service name is \"pfx3:CalculationsService\". servicePort: Specifies the service port for the SOAP request. In this case, the service port is \"CalculationsEndpoint1\". operation: Specifies the operation name for the SOAP request. In this case, the operation name is \"GetDisbursementAmounts\". soapAction: Specifies the SOAP action for the SOAP request. In this case, the SOAP action is \"/Services/CalculationsService.serviceagent/CalculationsEndpoint1/GetDisbursementAmounts\". endpointURL: Specifies the endpoint URL for the SOAP request. The endpoint URL is obtained from the \"%%Connection/WebService/CalculationServiceURL%%"\ connection resource. authScheme: Specifies the authentication scheme for the SOAP request. In this case, no authentication scheme is used.The pd:inputBindings section defines the input bindings for the InvokeService activity. It maps the input parameters of the SOAP request to the values from the input data.In this case, the input bindings are as follows: inputMessage: The input message for the SOAP request is mapped to the \"pfx4:DisbursementRequest\" element from the input data. pfx4:caseId: The value of the \"caseId\" element from the input data is mapped to the \"pfx4:caseId\" element in the SOAP request and the xsl:value-of is given as select=\"$Start/pfx4:DisbursementRequest/pfx4:caseId\". pfx4:applicationNumber: The value of the \"applicationNumber\" element from the input data is mapped to the \"pfx4:applicationNumber\" element in the SOAP request, the xsl:value-of is given as select=\"if (string-length($Start/pfx4:DisbursementRequest/pfx4:applicationNumber) = 0) then\n\t$GetApplicationNumber/resultSet/Record[1]/APLN_NBR\nelse\n\t$Start/pfx4:DisbursementRequest/pfx4:applicationNumber\ . If the \"applicationNumber\" element is empty, the value is obtained from the \"GetApplicationNumber\" process variable. pfx4:userId: The value of the \"userId\" element from the input data is mapped to the \"pfx4:userId\" element in the SOAP request the xsl:value-of is given as select=\"$Start/pfx4:DisbursementRequest/pfx4:userId\. pfx4:sender: The value of the \"sender\" element from the input data is mapped to the \"pfx4:sender\" element in the SOAP request the xsl:value-of is is given as select=\"$Start/pfx4:DisbursementRequest/pfx4:sender\. pfx4:autosave: The value \"true\" is mapped to the \"pfx4:autosave\" element in the SOAP request the xsl:value-of is given as select='\"true\"'. Overall, the InvokeService activity is configured to invoke a SOAP web service with the specified parameters and input bindings. The input values for the SOAP request are mapped from the input data and process variables.
                    """
                },
                {
                    "role": "user",
                    "content": input
                }
            ],
            "max_tokens": 5000,
            "temperature": 0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            "stop": None
        }
        headers = {
            "Content-Type": "application/json",
            "api-key": openai_key
        }
        
    
        response = self.session.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        response = response.json()
        print(response)
        content = {}
        for choice in response['choices']:
            if choice["index"] == 0 and choice["finish_reason"] == "stop":
                message = choice["message"]
                if message["role"] == "assistant":
                    content =message["content"]
                    content=content.replace("\n","")
                    content=content.replace("-","")
                    return content

