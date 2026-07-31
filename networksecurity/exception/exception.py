import sys


class NetworkSecurityException(Exception):
    def __init__(self, error_meassage, error_details:sys):
        self.error_message = error_meassage
        _,_,exc_tb = error_details.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in script: [{0}] at line number: [{1}] error message: [{2}]".format(
            self.file_name, self.line_number, self.error_message
        )