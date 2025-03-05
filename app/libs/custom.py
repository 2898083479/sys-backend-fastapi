import json
from cryptography.fernet import Fernet
from rich.console import Console

__all__ = (
    'cur_print',
    'encrypt',
    'decrypt',
    'serialize',
    'deserialize',
)

console = Console()


def cur_print(print_str: str, mode: str = 'l', end: str = '\n'):
    """
        自定义控制台输出, 使其能在输出的同时制定输出颜色\n
        :param print_str: 需要输出的字符串
        :param mode: 字体颜色: w: 警告warning 红色, sc: 成功success 绿色, t: 提示tips 黄色, p: 重要primary 蓝色, sd: 次要secondary 青蓝色, l: 日志log 白色
        :param end:
    """
    cs_p_c_t = {'w': 'red', 'sc': 'green', 't': 'yellow', 'p': 'blue', 'sd': 'cyan', 'l': 'white'}
    console.print(f'[bold {cs_p_c_t.get(mode)}]{print_str}', end=end)


def encrypt(origin: str, key: str):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(origin.encode('utf-8')).decode('utf-8')


def decrypt(encrypted: str, key: str) -> str:
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted.encode('utf-8')).decode('utf-8')


def serialize(obj: dict | list) -> str:
    """
    將字典列表序列化為字符串
    :param obj:
    :return:
    """
    return json.dumps(obj, ensure_ascii=False).encode('utf-8')


def deserialize(obj_str: str) -> dict:
    """
    將字符串反序列化為字典列表
    :param obj_str:
    :return:
    """
    return json.loads(obj_str)
