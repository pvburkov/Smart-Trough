BOT_TOKEN = '301887493:AAFdNXpQbbw_90cS8Ai7qfuquxejKILicZk'

WEBHOOK_HOST = '52.169.114.1'
WEBHOOK_PORT = 8443  
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert2.pem' 
WEBHOOK_SSL_PRIV = './webhook_pkey2.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (BOT_TOKEN)