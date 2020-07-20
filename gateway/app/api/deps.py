from fastapi import status


def map_error_code_to_status_code(error_code):
    statuses_mapping = {
        'NOT_FOUND': status.HTTP_404_NOT_FOUND,
        'VALIDATION_ERROR': status.HTTP_400_BAD_REQUEST,
        'BUSINESS_RULE_ERROR': status.HTTP_422_UNPROCESSABLE_ENTITY,
        'INTERNAL_SERVER_ERROR': status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return statuses_mapping.get(error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
