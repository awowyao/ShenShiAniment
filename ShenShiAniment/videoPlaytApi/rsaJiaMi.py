
import rsa
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)
    return key

def encrypt_data(msg):
    public_key = get_key('rsa_public_key.pem')
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(encrypt_msg):
    private_key = get_key('rsa_private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def test_encrypt_decrypt():
    msg = "coolpython.net"
    encrypt_text = encrypt_data(msg)
    print(encrypt_text)
    decrypt_text = decrypt_data(encrypt_text)

    print(msg == decrypt_text)


def long_decrypt(msg):
    msg = base64.b64decode(msg)
    rsa_private_key = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEA0glHxY4SFRNg66/QGn8OZfpcTToZQuAL2ib1Z0XpRK0j5aPy
        iO3KEUgTrn09q9Crgvihj8yOS2I+AmDpaaupcO4Kjl7/NRN0GI/ZC5up5qRH4B/r
        bOUtO2mLE9CwS9eWMlqdZzyQUxCSBMJPKGh2ksg0nwqDpiGxtPw9zjlrO2+odagu
        2GBkU43QhJmHaM6Cs9V0wa5hMvr6aW02H/YSfQlK47tA3j6zXSvAwfRU69pTk++w
        xhT9kbe9mND2VWhdPcoc58C51u18s10A8C+qVQ7vaEEko8C0ywlkQPs1voCTMmEx
        cVNMKYL3f+6F7/8FFXa4IWMvHNAABXzaiYYoXwIDAQABAoIBABKGpQdk2tPaRYZx
        MUuumoHrAL2crhVUlvCjPRDisFeeM5HFOAnurdyzKdR00Yq+uVIWq7feVOXxs8+y
        TDd437vJRn8WTy/95K1oV4s+Xx14rt1/xnYKPnoeFH/AvLwdaoiyFQfB5madPVpU
        G6oc9+oS5KlRwrKI1Rh5cA4pL5WQ86XQQb9LpirD39BpO18u1NIDXim4PSAP8uig
        8V5yIJXeKMUsbH+bZvisoWqj/RBaR4UsJTUufGxPf9qy7sQRSbNM1W1RErd/JoPn
        FV7y1SU+srcGSo003vvWEESfxwbYWZTiQR5PO1ir0FUfBuY6dBkJmizhtlxAP5lq
        PusRWskCgYEA06ORvrM6ldCpNoUlb6RAYCozTcfPx15g2BwuNYnfmw0k/d/pUR8N
        2a0IwB/sATS/F6Q93rxnaAGexMLGlEnuhARd1BNOU9mhkBQ/nHjfOdz8EP7X47fU
        Doe3y0/jUrCtpOIhX01hW9s3+TOaHmnhmV+ytSk3PspU65V20sVoqosCgYEA/g+2
        JOn/14b99e6UFfpc1eTqlmwncMylIIgC7IZzVUHfRvEdKFoXE6n41o7bP38xfTPr
        N1B8wRQZmjkyl4QL/C8rVDRpCy/Hmxs0VFFldlH6Fo1cv47DZJvKlRN+IeCQi4A8
        b/Nx95vEzC2WjtjzHPTebp3DHuLcn0D9YTpNd/0CgYEAhhIv6RwHeBLor1YnwhLO
        iV0ShSqYcRdTyHQJvfbqxYHNNlsbpj1C++vHCFbwnk7445QzcZ/u7g9gsgsl25j+
        VXmiqw/T5gCPfgOlzI0x9KkOsgGPaH3zA4VspIqmWqL8TeDG/WW60IMOcXsEHlI7
        DXt3bZZ/nfJ1W4yi6qEOTkMCgYEA3hRPzG67U+PNRNe6nIeP9Oy4XqrFwyUvxoL9
        w1E3qbP9/14udaJif67ZNHwFjLibQu1KU7zIgGIYiyYqYiVr8JIu1tlFZSDr41ph
        YL8R6N55tJL3Gv8pL127NJqoa+aHk1mR+u4bliyUV0IWVGGyCYLGmHzRHcOCxLaj
        hgTXyOUCgYA/eLUlI/ndLXctBwwPZzgJALM783BS2TPeqe6nhdQm9AmbajI3ynib
        brefJvyQdffvHn3DoNnqI6AG2cLMP+5ymmF6WxVQvF6vqFjFhDC7dOlbD2Zr3r28
        sjmFfIxm3AHv5SqYGKLPsVtNxagLbjOneV1KFiNU/S1UTtai5GdH5Q==
        -----END RSA PRIVATE KEY-----'''
    length = len(msg)
    default_length = 256
    # 私钥解密
    priobj = Cipher_pkcs1_v1_5.new(RSA.importKey(rsa_private_key))
    # 长度不用分段
    if length < default_length:
        return b''.join(priobj.decrypt(msg, b'xyz'))
    # 需要分段
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(priobj.decrypt(msg[offset:offset + default_length], b'xyz'))
        else:
            res.append(priobj.decrypt(msg[offset:], b'xyz'))
        offset += default_length

    return b''.join(res).decode('utf8')


print(long_decrypt(
    'X5THipGD1GXGoK5q54+Muh+Bem+qj/WwspI/jPBt9B8gC0HmpO3HflhLIr50GKfxXxNy03MI9Xjy31oaToZuFzK7Yy9FyhH2+ABZg6U3l/HAqOdq9WDWJ4yTZKEVkjyhZh/5iNzdnpe9S+6gXeXC+Ga3S9age+LP8yCWBn7opK/xcOWfjqjD+6lpMpPoa0dZKpeDcJyGo7wJ0Dqc3pwtI3omfrVeT+NYKqjpKcYEymz6KiVRL637VAdcAayHARNibLix8tnoHqwm+Y1XhBBXX4W1iwzmeAClx+iqJ6Q2bb8AoUFH/qfKiu1ebKpJ724kuO5VIooX6JRlu7JBlOFivBO6zNlZwci7wWHg4eTy6ZZiX0MWNsEWnTWYKLXu8Yt+aVf6ozEWrKIvjGvIiZdmSGPUUYC8/KAIsMCyzS8Wpr5SkxlPUq7lRIC4g3spTP8E43WyWJ1NYu9cLfx2k3e0Q6Q0ZHdiDPlpcCZsuUeEnEQnK5ejmJLqM2DRsmoGNqiWNS2dlYTMAfbjvNFNWkob7/kYTvjVGZB5hyQTnkeJqsa+/wB3/oXGuc4xrhT/fmvEXF3mq6ef/OfP8Nhdx/5f6sYEL1COWi9mnI0q+fOJz8I0v7Dnu2yAOqHLOhrIYBCS97apGltZDTjl4xytuMAKxpL3R9xoHp+I00b3xvmKUbO7NpTRhk+BIl0rT2Bmu2Y7UCqvfc5XQtNQJxCPmTGvhrf6h1zaJKs9nXErNeuHaHhlT5xE6T383BiSMfpFOSm/B+IP3zaAHVJy/wFD2wJjeIsyMyCkpx702VGzzdn5LheNa/pUsEE5FyGc/MNi4gwKMj9rSCo55c0DheHBqlXqh1Hv05yckbmQqmTkTX/2+Wf064ZPb2+CrKD9D3M/+8xA2lVZj8euqoJQoJVI8ld6fEsld6McHX6f0jhn/fAms1GVN6Vk0WDxCPVvqjWgG5+Ll+NMb236KEkLl6JLzfSCczY6SM1adUe+lv0iv8H56tlisB6J0QKYCU7Z5dyEWORM=='))
# test_encrypt_decrypt()     # True

# print(get_key('rsa_private_key.pem'))