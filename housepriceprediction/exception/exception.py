import os
import sys

class HousePricePredictionException(Exception):
    def __init__(self, error_message, error_detail:sys):
        self.error_message = error_message
        _,_,exb_tb = error_detail.exc_info()

        self.lineno = exb_tb.tb_lineno
        self.filename = exb_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: {self.filename} at line: {self.lineno} with message: {self.error_message}"
