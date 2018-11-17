# -*- coding: utf-8 -*-
"""
UniReq:
    UniReq extracts HTTP data and client information easily from DRF / Django
    for any cross client request.
    This package can handle requests from DRF requests, Django HTTP requests,
    mobile requests, chrome extensions requests, terminal requests, DRF Panel,
    API testers and more.

@author: aliasav
"""
import json
import logging
from rest_framework.parsers import JSONParser
from ipware.ip import get_real_ip

logger = logging.getLogger(__name__)

def get_client_details(request):
    '''
    Fetch client details
    '''
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    ip_addr = get_real_ip(request)
    user_agent = request.META['HTTP_USER_AGENT']
    resp = {
        'ip': ip_addr,
        'user-agent': user_agent,
    }
    return resp

def check_dict(the_dict, val):
    '''
    Check if an entity exists
    '''
    if val in the_dict:
        return the_dict[val]

def parse_request(request):
    '''
    Returns a dictionary of content from a request
    '''
    content = {}

    # POST request from mobile client
    try:
        # fetch data from request object
        # logger.debug("Trying to fetch data from request using JSONParser method")
        content = JSONParser().parse(request)

    except:

        # DRF panel
        try:
            # fetch data from _content parameter in drf request object
            # logger.debug("Trying to fetch data from request.POST['_content']")
            content = json.loads(request.POST["_content"])

        except:
            # POST request through web-site ajax request
            # logger.debug("Trying to fetch from request.POST")
            content = request.POST
            if request.FILES:
                content.update(request.FILES)

            # fetch data from request.data
            try:
                # logger.debug("Trying to fetch data from request.data")
                content = request.data
            except:
                logger.exception("Unable to fetch data from request.")

    # logger.debug("content in parse_request: %s\ttype: %s" %(content, type(content)))
    return content


"""
Accepts API name, request object, serializer, list of required_fields(optional), request_type(optional) 
Returns boolean valid_data flag and dictionary of required_fields/value pairs

Accepts a request object and a list of required fields,
checks for values of required fields list in the request content
and returns a dict of available fields & valid_data boolean flag
if all required_fields data is present in request 

*request type: 
By default is 1 -> serves POST data from clients
Type 2 -> serves data sent through DRF panel

* De-serialisation available in 2 types:
1. Using serializer to be provided as parameter ('serializer')
2. Custom serializer: for debugging purposes, points out particular field with missing data
"""

def get_request_content(api_name, request, serializer=None, required_fields=None, request_type=None):
    '''fetch content in dict -> de-serialise data if valid -> return is_valid flag and data'''

    data = {}
    valid_data_flag = True

    # parse request
    # fetch request data content in a dictionary
    content = parse_request(request)

    # proceed to de-serialisation of content

    # check for required_fields
    # if present, use custom de-serialisiation
    if required_fields:

        # custom de-serialisation
        # Points on particular field that is missing in request data
        # fill data with required fields
        # immediately exit & return false & empty dict if a particular field is not found

        for field in required_fields:

            # find value of field in request obj
            value = check_dict(content, field)
            data[field] = value

            # if not value:
            #     valid_data_flag = False
            #     logger.error("Field not present in request.\nAPI:%s\nField: %s\nRequest: %s\n"
            #                    %(api_name, field, content))
            #     return (valid_data_flag, {})
            # else:
            #     data[field] = value

        logger.info("Valid Content in request:\nAPI: %s\nContent: %s\n" %(api_name, data))
        return (valid_data_flag, data)

    # serializer de-serialisation
    # serializer sent to function as parameter 'serializer'
    elif serializer != None:

        # de-serialize content using serializer
        msg = "Serializer for {0}: {1}".format(api_name, serializer)
        logger.debug(msg)
        serializer_data = serializer(data=content)
        valid_data_flag = serializer_data.is_valid()
        data = serializer_data.data

        if valid_data_flag:
            msg = "Valid Content in request:\nAPI: {0}\nContent: {1}\n".format(api_name, data)
            logger.info(msg)
            return (valid_data_flag, data)
        else:
            msg = "In-valid Content in request:\nAPI: {0}\nContent: {1}\n".format(api_name, content)
            logger.info(msg)
            return (valid_data_flag, data)

    logger.error("Missing serializer in get_request_content")
    return (False, None)
