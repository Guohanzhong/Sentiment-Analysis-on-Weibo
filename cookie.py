import binascii
import base64
import requests
import urllib.request
import urllib
import re
import rsa

def Prelogin(prelogin_url):
    data = requests.get(prelogin_url).content.decode('utf-8')
    p = re.compile('\((.*)\)')
    data_str = p.search(data).group(1)
    server_data_dict = eval(data_str)
    pubkey = server_data_dict['pubkey']
    servertime = server_data_dict['servertime']
    nonce = server_data_dict['nonce']
    rsakv = server_data_dict['rsakv']
    return pubkey, servertime, nonce, rsakv



def PostData(username, password, pubkey, servertime, nonce, rsakv):
    su, sp = RSAEncoder(username, password, pubkey, servertime, nonce)
    post_data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': '',
        'prelt': '645',
        'pwencode': 'rsa2',
        'returntype': 'META',
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': str(servertime),
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': su,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', #noqa
        'useticket': '1',
        'vsnf': '1',
    }
    return post_data




def RSAEncoder(username, password, pubkey, servertime, nonce):
    su_url = urllib.parse.quote_plus(username)
    su_encoded = su_url.encode('utf-8')
    su = base64.b64encode(su_encoded)
    su = su.decode('utf-8')
    rsaPublickey = int(pubkey, 16)
    e = int('10001', 16)
    key = rsa.PublicKey(rsaPublickey, e)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    password = rsa.encrypt(message.encode('utf-8'), key)
    sp = binascii.b2a_hex(password)
    return su, sp