class CustomValidationError(Exception):

    def __init__(self, message=''):
        super().__init__(message)
        self._has_errors = False
        self._code = '0'
        self._description = message
        self._validations = None

    def __iter__(self):
        yield 'code', self._code
        yield 'description', self._description
        yield 'validations', self._validations

    def as_dict(self):
        return dict(self)

    @property
    def has_errors(self):
        return self._has_errors

    @property
    def code(self):
        return self._code

    @property
    def description(self):
        return self._description

    @property
    def validations(self):
        return self._validations

    def set_error(self, code, description, validations=None):
        self._has_errors = True
        self._code = code
        self._description = description
        self._validations = validations

    def set_not_found_error(self, message):
        self.set_error('NOT_FOUND', message)

    def set_validation_error(self, message, validations):
        self.set_error('VALIDATION_ERROR', message, validations)

    def set_business_rule_error(self, message):
        self.set_error('BUSINESS_RULE_ERROR', message)
