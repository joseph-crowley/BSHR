class QueryProcessingError(Exception):
    """Exception raised for errors in the query processing module."""
    def __init__(self, message="Error occurred in query processing"):
        self.message = message
        super().__init__(self.message)

class HypothesisGenerationError(Exception):
    """Exception raised for errors in the hypothesis generation."""
    def __init__(self, message="Error occurred in hypothesis generation"):
        self.message = message
        super().__init__(self.message)

class ExternalAPIError(Exception):
    """Exception raised for errors when interacting with external APIs."""
    def __init__(self, message="Error occurred with an external API"):
        self.message = message
        super().__init__(self.message)
