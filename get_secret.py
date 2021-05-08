import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, ChainedTokenCredential, AzureCliCredential
from azure.core.exceptions import HttpResponseError


# Run run.get.secret.ps1 to initialize environment variables and run the app
"""
Manual: 
In Windows, using PowerShell, you can get and set temporary environment vars 
thusly: 
    set: $env:VAULT_URL="https://keyvault-pythonqs-kv.vault.azure.net/"
    get: $env:VAULT_URL
In Linux: 
    set: export VAULT_URL="https://keyvault-pythonqs-kv.vault.azure.net/"
    get: echo $VAULT_URL

"""
VAULT_URL = os.environ["VAULT_URL"]
SECRET_NAME = os.environ["SECRET_NAME"]
# credential = DefaultAzureCredential()
# This seems to work better: 
# https://docs.microsoft.com/en-us/answers/questions/74848/access-denied-to-first-party-service.html
credential = ChainedTokenCredential(AzureCliCredential())
client = SecretClient(vault_url=VAULT_URL, credential=credential)

try:
    # Let's get the secret using its name
    print("\n.. Get a Secret by name")
    the_secret = client.get_secret(SECRET_NAME)
    print("Secret with name '{0}' was found with value '{1}'.".format(
        the_secret.name, the_secret.value))
except HttpResponseError as e:
    print("\nThis sample has caught an error. {0}".format(e.message))
