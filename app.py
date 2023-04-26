import os
import logging
import yaml

#from webexteamssdk import WebexTeamsAPI
from webex_bot.webex_bot import WebexBot
from openai_command import OpenAiCommand


log = logging.getLogger(__name__)


CONFIG_FILE_LOCATION = "~/.openai_bot.yml"

def parse_yaml_config(config_file_path):
    if not os.path.isfile(config_file_path):
        log.warn(f"Config file '{config_file_path}' not found.")
        return None

    config_dict = None
    with open(config_file_path, 'r') as file:
        try:
            config_dict = yaml.load(file, Loader=yaml.FullLoader)
            print(config_dict)
        except yaml.YAMLError as exc:
            log.warning("Error reading config file: "+ exc)
            return None
    return config_dict


# Gather our required inputs
config = parse_yaml_config(os.path.expanduser(CONFIG_FILE_LOCATION))
log.warning(f"Config Type is {type(config)}")
if config is None:
    config = dict();

log.info(config);

webex_email = os.getenv('WEBEX_EMAIL')
if webex_email is not None:
    config['webex_email'] = webex_email

access_token = os.getenv('WEBEX_TEAMS_ACCESS_TOKEN')
if access_token is not None:
    config['webex_token'] = access_token

openai_token = os.getenv('OPENAI_API_KEY')
if openai_token is not None:
    config['openai_token'] = openai_token


# Make sure we have everything we need
if config.get('webex_email') is None:
    log.error(f"The webex email is not found in the config file {CONFIG_FILE_LOCATION} or the environment var WEBEX_EMAIL")
    exit(3);

if config.get('webex_token') is None:
    log.error(f"The webex token is not found in the config file {CONFIG_FILE_LOCATION} or the environment var WEBEX_TEAMS_ACCESS_TOKEN")
    exit(1);

if config.get('openai_token') is None:
    log.error(f"The openai token is not found in the config file {CONFIG_FILE_LOCATION} or the environment var OPENAI_API_KEY")
    exit(2);



# Create a Bot Object
bot = WebexBot(teams_bot_token=config['webex_token'],
               approved_users=[config['webex_email']],
               bot_name="OpenAI Bot",
               include_demo_commands=False)

# webex_api = WebexTeamsAPI(access_token=config['access_token'])

# Grab your API over at https://beta.openai.com/account/api-keys
bot.commands.clear()
bot.add_command(OpenAiCommand(config['openai_token']))
bot.help_command = OpenAiCommand(config['openai_token'])

bot.run()
