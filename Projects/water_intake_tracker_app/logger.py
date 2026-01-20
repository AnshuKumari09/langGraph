import logging  ##built-in logger,log likhne ke tools
# Logger ko rules batana
# Matlab:
# log kab likhne hain,kis format me likhne hain,kaunsi cheezein dikhani hain
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
)
# | Part            | Matlab          |
# | --------------- | --------------- |
# | `%(asctime)s`   | Date + Time     |
# | `%(levelname)s` | INFO / ERROR    |
# | `%(message)s`   | Tumhara message |


def log_message(message):
    logging.info(message)

# Tum sirf message doge,Andar se logger use hoga
def log_error(message):
    logging.error(message)