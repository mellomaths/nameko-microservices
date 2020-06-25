statuses_mapping = {
    'NOT_FOUND': 404,
    'VALIDATION_ERROR': 400,
    'BUSINESS_RULE_ERROR': 422,
    'INTERNAL_SERVER_ERROR': 500
}


def map_error_code_to_status_code(error_code):
    return statuses_mapping.get(error_code, 500)
