from flask import jsonify
from dicttoxml import dicttoxml

def dict_to_xml(object):
	""" Return an xml version of a dict. """
	return dicttoxml(object, attr_type=False, root=False)

# Successful responses 2xx:

def return_object(object, accept_type):
	""" Successfully return a jsonified version of an object. """
	status_code = 200
	if accept_type == "application/json":
		return jsonify(object), status_code
	else:
		return dict_to_xml(object), status_code, {'Content-Type': accept_type}

def return_analytics(accept_type):
	""" Successfully return info that the analytics have been provided. """
	status_code = 200
	response = {"response": "Analytics provided in a new tab"}
	if accept_type == "application/json":
		return jsonify(response), status_code
	else:
		return dict_to_xml(response), status_code, {'Content-Type': accept_type}

# Client error responses 4xx:

def error(message, status_code):
	""" Wrapper method to send an error response. """
	return jsonify(error=message), status_code

def field_names_incorrect():
	""" At least one of the actual field names (e.g. "typ" instead of "type")
	is incorrect and the request can therefore not be understood. """
	return error("One or more field names are incorrect. ", 400)

def resource_not_found():
	""" The sent resource is not contained in the database. """
	return error("The expected resourse is not contained in the database. ", 404)

def resources_not_found():
	""" Atleast 1 of the sent resource is not contained in the database. """
	return error("One or more of the expected resourses is not contained in the database. ", 404)

# Server error responses: 5xx:

def server_error():
	""" An unexpected server error occured. """
	return error("There was an unexpected server error. ", 500)
