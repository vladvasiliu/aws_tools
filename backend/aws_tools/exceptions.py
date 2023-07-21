class ResourceNotFoundException(Exception):
    def __init__(self, aws_resource):
        self.aws_resource = aws_resource


class RDSInvalidState(Exception):
    pass
