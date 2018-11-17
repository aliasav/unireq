=====
Unireq
=====

UniReq extracts HTTP data and client information easily from DRF / Django
for any cross client request.

This package can handle requests from DRF requests, Django HTTP requests,
mobile requests, chrome extensions requests, terminal requests, DRF Panel,
API testers and more.

Quick start
-----------

pip install -r requirements.txt
pip install unireq

Usage
-----------

from request_utils import parse_request, get_client_details

# get all POST data in the request
data = parse_request(request)

# get clint details
data['client_details'] = get_client_details(request)
