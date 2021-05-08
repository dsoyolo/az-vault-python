import os
import cmd
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, ChainedTokenCredential, AzureCliCredential


"""
In Windows, using PowerShell, you can get and set temporary environment vars 
thusly: 
    set: $env:KEY_VAULT_NAME="KeyVault-PythonQS-kv"
    get: $env:KEY_VAULT_NAME
In Linux: 
    set: export KEY_VAULT_NAME="KeyVault-PythonQS-kv"
    get: echo $KEY_VAULT_NAME
"""
keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

#credential = DefaultAzureCredential()
# This seems to work better: 
# https://docs.microsoft.com/en-us/answers/questions/74848/access-denied-to-first-party-service.html
credential = ChainedTokenCredential(AzureCliCredential())
client = SecretClient(vault_url=KVUri, credential=credential)

secretName = input("Input a name for your secret > ")
secretValue = input("Input a value for your secret > ")

print(
    f"\nCreating a secret in {keyVaultName} called '{secretName}' with the value '{secretValue}' ...")
client.set_secret(secretName, secretValue)
print(" done.")

print(f"\nRetrieving your secret from {keyVaultName}.")
retrieved_secret = client.get_secret(secretName)
print(f"Your secret is '{retrieved_secret.value}'.")

print(f"\nDeleting your secret from {keyVaultName} ...")
poller = client.begin_delete_secret(secretName)
deleted_secret_uri = poller.result()
print(" done.")
