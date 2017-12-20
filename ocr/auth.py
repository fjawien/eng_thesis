from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
def get_vision(oauth2_creds_filename, service_url=DISCOVERY_URL):
    """
    Read oauth2 credentials and return a Google service object,
      which you can then invoke like this:

    ("vision" is the service object)
    request = vision.images().annotate(body={'requests': img_requests_data})
    vision_response_dict = request.execute(num_retries=5)

    """
    creds = GoogleCredentials.from_stream(oauth2_creds_filename)
    service = discovery.build('vision', 'v1', credentials=creds,
                              discoveryServiceUrl=DISCOVERY_URL)
    return service