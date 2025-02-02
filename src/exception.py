import sys
import logging
import os

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Function to capture error details
def error_message_details(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_detail_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_detail_message


# Custom Exception Class
class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):  # fixed argument name
        super().__init__(error_message)
        self.error_details = error_message_details(error_message, error_details=error_details)  # fixed argument name

    def __str__(self):
        return self.error_details


# Configure logging (save logs in the logs folder)
logging.basicConfig(
    filename=os.path.join('logs', 'error_log.log'),
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)

# Main execution
if __name__ == "__main__":
    try:
        a = 1 / 0  # This will raise ZeroDivisionError
    except Exception as e:
        logging.info("Exception occurred: Division by 0")
        logging.shutdown()  # Ensures the logs are written
        raise CustomException(e, sys)
