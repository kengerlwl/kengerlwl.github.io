import re
import os
import 加密算法.mymd5 as md5
import requests
from PIL import Image
from Config import *

# 这里是我的代理， 如果不需要代理删除这个就行，
proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}  # 设置http和https 代理

# 转换后的图片url前缀
github_url = None
md_name = None
md_name_hash = None
content = None
md_file = None
img_dir_pre = None  # 图片存储的目录
conf = get_config()

# 文件夹路径
out_path = 'copyMDout输出'

def request_download(path, IMAGE_URL):
    """
    :param path: 被存储到的路径
    :param IMAGE_URL: 图片的url
    :return:
    """
    if conf['proxy']:
        r = requests.get(IMAGE_URL, proxies=proxies)  # 使用代理   ！！！！！！！ 也可以不用，我是境外的网站所以要用
    else:
        r = requests.get(IMAGE_URL)
    with open(path, 'wb') as f:
        f.write(r.content)


def init():
    global github_url
    global md_name
    global content
    global md_file
    global img_dir_pre
    global md_name_hash

    # 使用raw GitHub源而不是CDN
    github_url = 'https://raw.githubusercontent.com/' + conf['username'] + '/' + conf['repository'] + '/master'
   
    print('github image url 的链接前缀 ： ' + github_url)

    md_name = conf['md_name']
    md_name_hash = md5.my_md5(md_name)
    img_dir_pre = FileDir + '/image/' + md_name_hash + '/'

    # 新建可能需要的目录
    os.makedirs(FileDir + '/image/', exist_ok=True)
    os.makedirs(FileDir + '/'+out_path+'/', exist_ok=True)
    os.makedirs(FileDir + '/image/' + md_name_hash, exist_ok=True)

    # 打开待处理文件夹
    with open(conf['complete_name'], 'r', encoding='utf-8', errors='ignore') as f:
        content = f.readlines()

    md_file = open(conf['complete_name'], 'w', encoding='utf-8', )


def img_pro(img_url):
    global github_url
    global md_name
    global content
    global md_file
    global img_dir_pre
    global md_name_hash

    # 处理相对路径
    if img_url.startswith("../") or img_url.startswith("./") or img_url.startswith("../../") or not img_url.startswith("http"):
        # 如果是相对路径，需要找到实际的图片文件
        post_format = img_url.split(".")[-1]  # 图片格式
        post_format_s = post_format.split("?")
        # 去除结尾的?的后缀
        if len(post_format_s) >= 2:
            post_format = post_format_s[0]

        new_local_img_path = img_dir_pre + md5.my_md5(img_url) + '.' + post_format
        new_github_img_path = github_url + '/image/' + md_name_hash + '/' + md5.my_md5(img_url) + '.' + post_format

        # 尝试找到实际的图片文件路径
        actual_img_path = None

        # 方法1: 从当前md文件位置出发的相对路径
        if conf['complete_name']:
            md_dir = os.path.dirname(os.path.abspath(conf['complete_name']))
            relative_path_from_md = os.path.normpath(os.path.join(md_dir, img_url))
            if os.path.exists(relative_path_from_md):
                actual_img_path = relative_path_from_md
                print(f"找到图片(相对于MD文件): {actual_img_path}")

        # 方法2: 从项目根目录出发的相对路径
        if actual_img_path is None:
            project_root = os.path.abspath(FileDir)
            relative_path_from_root = os.path.normpath(os.path.join(project_root, img_url))
            if os.path.exists(relative_path_from_root):
                actual_img_path = relative_path_from_root
                print(f"找到图片(相对于项目根目录): {actual_img_path}")

        # 方法3: 从当前工作目录出发的相对路径
        if actual_img_path is None:
            cwd_path = os.path.normpath(os.path.join(os.getcwd(), img_url))
            if os.path.exists(cwd_path):
                actual_img_path = cwd_path
                print(f"找到图片(相对于当前工作目录): {actual_img_path}")

        # 方法4: 直接作为绝对路径
        if actual_img_path is None and os.path.exists(img_url):
            actual_img_path = os.path.abspath(img_url)
            print(f"找到图片(直接路径): {actual_img_path}")

        # 方法5: 尝试去掉开头的相对路径符号，直接从项目根目录查找
        if actual_img_path is None:
            clean_path = img_url.lstrip('./').lstrip('../')
            if clean_path != img_url:  # 确实有相对路径符号被去掉
                project_root = os.path.abspath(FileDir)
                clean_full_path = os.path.normpath(os.path.join(project_root, clean_path))
                if os.path.exists(clean_full_path):
                    actual_img_path = clean_full_path
                    print(f"找到图片(清理路径后): {actual_img_path}")

        # 如果找到了实际的图片文件，复制到目标位置
        if actual_img_path and os.path.exists(actual_img_path):
            try:
                img = Image.open(actual_img_path)
                img.save(new_local_img_path, post_format)
                print(f"成功处理图片: {img_url} -> {new_local_img_path}")
            except Exception as e:
                print(f"无法处理图片 {actual_img_path}: {str(e)}")
        else:
            print(f"警告: 找不到图片文件 {img_url}")

        return new_github_img_path

    # 原有逻辑处理
    post_format = img_url.split(".")[-1] # 图片格式可能不是png结尾
    post_format_s = post_format.split("?")
    # 去除结尾的?的后缀
    if len(post_format_s) >= 2:
        post_format = post_format_s[0]
    new_local_img_path = img_dir_pre + md5.my_md5(img_url) +'.'+ post_format
    new_github_img_path = github_url + '/image/' + md_name_hash +'/' + md5.my_md5(img_url) +'.' + post_format
    # http 图片
    if re.findall('http', img_url) != []:
        request_download(new_local_img_path , img_url)

    # 本地的图片
    else:
        try:
            img = Image.open(img_url)
            img.save(new_local_img_path, post_format)
        except Exception as e:
            print(f"无法处理图片 {img_url}: {str(e)}")
            # 如果无法处理，仍然返回新路径
            pass

    return new_github_img_path


def main():
    global github_url
    global md_name
    global content
    global md_file
    global img_dir_pre

    for line in content:
        image_urls = re.findall(r'!\[.*\]\((.*)\)', line)  # 检验有没有图片,并提取出来
        # print(image_urls)
        if image_urls != []:
            # print(image_urls)
            try:
                image_url = image_urls[0]
                print(image_url)
                if image_url.find("raw.githubusercontent.com") != -1:
                    raise Exception("已经是raw github图源了")
                if image_url.find("cdn.jsdelivr.net/gh") != -1:
                    # 将CDN链接转换为raw GitHub源
                    line = line.replace("cdn.jsdelivr.net/gh", "raw.githubusercontent.com")
                    line = line.replace("/image/", "/master/image/")
                    raise Exception("已将CDN切换为raw Github图源")
                    

                # if image_url.find("cdn.jsdelivr.net") != -1:
                #     raise Exception("已经是github的cdn图源了")
                

                git_url = img_pro(image_url)
                print(git_url)
                line = line.replace(image_url, git_url)
            except Exception as e:
                print(e)
                pass
        else:
            pass
        md_file.write(line)


if __name__ == '__main__':


    conf['md_name'] = "test.md"
    conf['complete_name'] = "./test.md"
    init()
    main()
