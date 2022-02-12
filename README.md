# ZXHN-F650-crack
获取中兴光猫ZXHN F650/F450A 超级用户密码

## Info
- Tested on ZXHN F650 V2.0.0P1T3
- Tested on ZXHN F450A V2.0.0P1T1sh

F450A 在利用 copy 时需多传入一个 token 字符串，但是当前版本传入空串也可以，疑似bug

如果这个bug后续被修复，token 的值可以从 `UrlTokenPage` 对应的页面中 parse 得到

## Usage
- python3 main.py
- Input password for user "useradmin"

## Requirements
- Python3
- requests

## Acknowledgements
- [中兴光猫配置文件db_user_cfg.xml结构分析及解密](https://www.52pojie.cn/thread-1005978-1-1.html)
- [voidxxl7/ZXHN-F650-PassReader](https://github.com/voidxxl7/ZXHN-F650-PassReader)


## Licenses
License: MIT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
