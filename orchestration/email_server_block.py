import sys
from prefect_email import EmailServerCredentials
sys.path.append('./')
from utils.config_reader import Config

conf = Config()

credentials = EmailServerCredentials(
    username=conf.config["EMAIL-ADDRESS-PLACEHOLDER"],
    password=conf.config["PASSWORD-PLACEHOLDER"],
)
credentials.save("email-notifier", overwrite = True)
