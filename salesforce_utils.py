from simple_salesforce import Salesforce
import xml.etree.ElementTree as ET

def connect_to_salesforce(username, password, security_token):
    try:
        sf = Salesforce(username=username, password=password, security_token=security_token)
        return sf
    except Exception as e:
        raise Exception(f"Failed to connect to Salesforce: {str(e)}")

def get_metadata_types(sf):
    try:
        # Retrieve metadata types using the Metadata API
        result = sf.restful('services/data/v52.0/metadata/describe')
        return [metadata_type['xmlName'] for metadata_type in result['metadataObjects']]
    except Exception as e:
        raise Exception(f"Failed to retrieve metadata types: {str(e)}")

def get_metadata(sf, metadata_types):
    metadata = {}
    for metadata_type in metadata_types:
        try:
            # Retrieve metadata for each type using the Metadata API
            result = sf.restful(f'services/data/v52.0/metadata/{metadata_type}')
            metadata[metadata_type] = result['records']
        except Exception as e:
            raise Exception(f"Failed to retrieve metadata for {metadata_type}: {str(e)}")
    return metadata

def parse_metadata(metadata):
    parsed_metadata = {}
    for metadata_type, items in metadata.items():
        parsed_metadata[metadata_type] = {}
        for item in items:
            name = item['fullName']
            parsed_metadata[metadata_type][name] = parse_xml(item['content'])
    return parsed_metadata

def parse_xml(xml_content):
    root = ET.fromstring(xml_content)
    return xml_to_dict(root)

def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result
