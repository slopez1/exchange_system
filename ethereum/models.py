from django.db import models

# Create your models here.



class Config(models.Model):
    node_url = models.CharField(max_length=1000)            # Url to node provider
    account_path = models.CharField(max_length=1000)        # Path to account file
    keystore_password = models.CharField(max_length=1000, blank=True)   # Password to unlock UTF account
    smc_address = models.CharField(max_length=1000)         # Ethereum address to SMART CONTRACT
