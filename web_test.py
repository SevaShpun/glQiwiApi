from glQiwiApi import QiwiWrapper

Y_TOKEN = '4100116602400968.8768F11B3A3EBA77AD840322D6DF69C24379DA18D2B0FB63C8B666F2BD78E957739B00D90D8F71F25762D06D513B7528BC4A8BBF16E157645E64EFBCA71922C08C2A882BC1FB9B9A329BD20752201037ECC01A75C117F77C1D761B4FAF895920302C81F685A9C875959C8B72E312BAEDE701090C10EABA279B92777E85E3F171'
TOKEN = '4cb242f9ead43bd0e1e98eb7c442262f'
WALLET = '+380968317459'
QIWI_SECRET = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImJuMXZmNy0wMCIsInVzZXJfaWQiOiIzODA5NjgzMTc0NTkiLCJzZWNyZXQiOiI2ZmVjYzA4ZWEyOTgxMDY3N2VkNDU1YjY3MTVhZjc3ZjRhMjY4Yzc5MDU0ZGI2ZmYyZTEzZjI1Njk5ODQ3M2ZmIn19'
wallet = QiwiWrapper(
    api_access_token=TOKEN
)


@wallet.transaction_handler()
async def main(event):
    print(event)


wallet.start_polling()

# asyncio.run(main())
