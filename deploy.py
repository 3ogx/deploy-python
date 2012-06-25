#!/usr/bin/python
# -*- coding:utf-8 -*-
# -*- mode:python -*-

import os,sys,datetime
import re
prompt = ">"

deploy = 'dev'
for val in sys.argv:
    if (re.search('public',val.lower()) != None):
        deploy = 'public'
    if (re.search('test', val.lower()) != None):
        deploy = 'test'

if (deploy == 'dev'):
    # 網站根目錄
    webroot_path = '/Users/beiwei/Sites/deploydemo'
    # 壓縮包存放目錄
    package_path = '/Users/beiwei/Sites/'
    # 請留空
    package_name = ''
    # 部署源碼目錄
    resource_path   = '/Users/beiwei/Sites/deploy/'
    # 框架路徑
    framework_path  = '/Users/beiwei/Sites/yii/framework'


# 解壓縮文件
def _unzip_package(pkg_path, extra_path):
    global package_name

    while True:
        print "請輸入要發佈的包名稱："
        _package_name = raw_input(prompt)
        if (_package_name): break

    print "確認要發佈的版本為 %s? [y/n]" % _package_name
    _confirm = raw_input(prompt)
    if (_confirm.lower() == 'n'):
        print '%s 包已經取消發佈' % _package_name
        return

    if (os.path.exists(pkg_path + _package_name)):
        try:
            _tmp_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            package_name = _tmp_name
            os.rename(pkg_path + _package_name, extra_path + package_name + '.zip')
            os.mkdir(extra_path + package_name)
            if (os.path.exists(extra_path + package_name)):
                os.system('unzip -qo %s%s -d %s' % (extra_path, package_name, extra_path + package_name))

            # 刪除包文件
            # os.remove(extra_path + package_name + '.zip')
        except IOError as e:
            print '({0}): {1}'.format(e.errno, e.strerror)
            exit(0)
        except (RuntimeError, TypeError, NameError, ValueError):
            print 'error'
            exit(0)
    else:
        print '%s 下不存在文件 %s' % (package_path, _package_name)
        exit(0)



# 創建符號鏈接
def _create_symbolic_link(deploy_dir):
    global package_name,framework_path

    # 框架的符號鏈接地址
    _framework_link = os.path.join(deploy_dir, package_name, 'framework')
    if not os.path.islink(_framework_link):
        os.symlink(framework_path, _framework_link)

    # 刪除網站路徑的符號鏈接，建立新發佈版本
    if os.path.islink(webroot_path):
        os.unlink(webroot_path)
    os.symlink(os.path.join(deploy_dir, package_name), webroot_path)



# 創建臨時目錄
def _create_tmp_file(extra_path):
    global package_name

    if not package_name:
        print '壓縮包錯誤！'
        return

    tmp_files = {
        '_runtime_file': os.path.join(extra_path, package_name, 'protected/runtime/'),
        '_assets_file': os.path.join(extra_path, package_name, 'apps/assets/'),
        '_themes_file': os.path.join(extra_path, package_name, 'apps/themes/')
        }
    for val in tmp_files.viewvalues():
        if not os.path.isdir(val):
            os.makedirs(val)
        os.chmod(val,0777)


# run
if __name__ == "__main__":
    _unzip_package(package_path, resource_path)
    _create_tmp_file(resource_path)
    _create_symbolic_link(resource_path)
