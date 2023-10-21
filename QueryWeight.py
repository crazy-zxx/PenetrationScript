#!/usr/bin/env python3

"""
安装依赖：
pip install requests beautifulsoup4
"""

import argparse
import multiprocessing
import os.path
import re

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", dest="domain", help="Single target domain (e.g. \"www.site.com\")")
parser.add_argument("-r", '--readfile', dest="readfile", help="Load domains from a file")
parser.add_argument('-v', "--version", dest="version", action="store_true",
                    help="Show program's version number and exit")
args = parser.parse_args()

__version = 1.0


def show_version():
    print(__version)


def check_domain(input_str: str):
    # 定义一个正则表达式来匹配域名
    domain_pattern = r'(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'

    # 使用正则表达式匹配输入字符串
    match = re.search(domain_pattern, input_str)

    if match:
        # 如果匹配成功，提取域名
        domain = match.group(2)
        return domain
    else:
        # 如果没有匹配到域名，返回 None 或者你想要的错误信息
        return None


# 提取指定id值的a标签，并获取其img子标签的alt值
def get_value(soup: BeautifulSoup, id: str):
    # 使用find方法查找具有指定id值的超链接
    link_with_id_x = soup.find(name='a', id=id)
    # 获取子标签img的alt属性值
    img_alt_value = link_with_id_x.find('img')['alt']
    return img_alt_value


# 补天：百度或移动大于等于1或者谷歌大于等于3
def check_butian(value: dict):
    if value['baidurank_br'] >= 1 or value['baidurank_mbr'] >= 1 or value['google_pr'] >= 3:
        return '满足补天要求！'
    else:
        return None


def query(domain: str):
    server_url = 'https://www.aizhan.com/cha/'
    domain = check_domain(domain)
    if domain:
        try:
            # 发送 GET 请求
            query_url = server_url + domain + '/'
            # 定义自定义请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36',
            }
            response = requests.get(url=query_url, headers=headers)
            # 检查响应状态码
            if response.status_code == 200:
                # 使用Beautiful Soup解析网页内容
                soup = BeautifulSoup(response.text, 'html.parser')

                # 权重项目
                id_weight = {
                    'baidurank_br': 0,  # 百度权重
                    'baidurank_mbr': 0,  # 移动权重
                    'google_pr': 0,  # 谷歌PR
                }

                # 搜索响应页面html，获取权重
                for k in id_weight.keys():
                    id_weight[k] = int(get_value(soup, k))

                # 控制台输出
                print(domain, '----',
                      f"百度权重:{id_weight['baidurank_br']}, 移动权重:{id_weight['baidurank_mbr']}, 谷歌PR:{id_weight['google_pr']}",
                      '----', check_butian(id_weight))

            else:
                print(f"请求失败，状态码：{response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"发生异常: {e}")


def batch_query_by_multi_proc(file: str):
    if os.path.exists(file):
        # 创建一个进程池，指定要使用的进程数量（根据CPU核心数或需求进行调整）
        num_processes = multiprocessing.cpu_count()  # 获取CPU核心数
        process_pool = multiprocessing.Pool(processes=num_processes)

        with open(file, 'r') as f:
            # 使用进程池并行执行任务
            process_pool.map(query, f.readlines())
            # 关闭进程池，等待所有进程完成
            process_pool.close()
            process_pool.join()
    else:
        print('文件不存在！')


if __name__ == '__main__':

    if not args.version and not args.domain and not args.readfile:
        parser.print_help()

    else:
        if args.domain:
            query(args.domain)

        elif args.readfile:
            batch_query_by_multi_proc(args.readfile)

        elif args.version:
            show_version()
