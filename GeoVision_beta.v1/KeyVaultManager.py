import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def retrieveKey(key):
    try:
         keyVault = os.environ.get('KEY_VAULT_NAME')
         vUrl = f"https://{keyVault}.vault.azure.net"
         vaultCredential = DefaultAzureCredential()
         keyVault_client = SecretClient(vault_url=vUrl, credential=vaultCredential)
         connect_key = keyVault_client.get_secret(key)
         return connect_key

    except Exception as err:
         print(f"There is an issue with the key vault client: {err}")