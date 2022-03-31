import logging

class DevBlogLogger(logging.Formatter):
    """Custom logger for outputting logs with a server_time attribute in the format"""

    default_time_format = '%d/%b/%Y %H:%M:%S'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record) -> str:
        if self.uses_server_time() and not hasattr(record, "server_time"):
            record.server_time = self.formatTime(record, self.default_time_format)

        return super().format(record)
    
    def uses_server_time(self):
        return self._fmt.find("{server_time}") >= 0