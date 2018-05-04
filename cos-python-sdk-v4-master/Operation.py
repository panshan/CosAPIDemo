#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
from qcloud_cos import UploadSliceFileRequest
from qcloud_cos import UploadFileFromBufferRequest
from qcloud_cos import UploadSliceFileFromBufferRequest
from qcloud_cos import UpdateFileRequest
from qcloud_cos import UpdateFolderRequest

from qcloud_cos import DownloadFileRequest

from qcloud_cos import DelFileRequest
from qcloud_cos import DelFolderRequest
from qcloud_cos import CreateFolderRequest
from qcloud_cos import StatFileRequest
from qcloud_cos import StatFolderRequest
from qcloud_cos import ListFolderRequest

import os, os.path

import logging
import sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

logger = logging.getLogger(__name__)

'''
生成cos的client并返回
'''
def getClient(app_id, secret_id, secret_key, region):
    client = CosClient(app_id, secret_id, secret_key, region)
    
    return client

'''
上传简单文件，如果cos上文件存在，则返回错误
主要用于小文件上传
'''
def uploadSimpleFile(bucket, client, localPath, cosPath):
    request = UploadFileRequest(bucket, cosPath, localPath)
    request.set_insert_only(0)  # 设置允许覆盖
    ret = client.upload_file(request)
    
    logger.info("uploadSimpleFile, return message: " + str(ret))
    return 0

'''
分片上传大文件，默认不覆盖
'''
def uploadBigFile(bucket, client, localPath, cosPath):
    request = UploadSliceFileRequest(bucket, cosPath, localPath)
    request.set_insert_only(0)  # 设置允许覆盖
    ret = client.upload_slice_file(request)

    logger.info("uploadBigFile, return message: " + str(ret))
    return 0

'''
下载文件
'''
def downloadFile(bucket, client, localPath, cosPath):
    request = DownloadFileRequest(bucket, cosPath, localPath)
    ret = client.download_file(request)

    logger.info("downloadFile, return message: " + str(ret))
    return 0

'''
上传文件夹到cos,cosRoot必须存在
cos平台可以一次创建多及目录，但路径参数必须以"/"结束
上传文件过程中，cos路径参数不能以"/"结束
'''
def uploadDir(bucket, client, localPath, cosPath):
    if os.path.isfile(localDir):    # 如果当前路径代表文件，则直接上传
        uploadBigFile(bucket, client, localPath, cosPath)
        return 0
    else:                           # 否则，创建目录，递归
        request = CreateFolderRequest(bucket, localDir)
        ret = client.create_folder(request)

        files = os.listdir(localDir)    # 列出当前目录下的文件
        for file in files:
            uploadDir(bucket, client, localDir + "/" + file, cosRoot + "/" + file)
    
def cos_demo():
    
    ############################################################################
    # 目录操作                                                                 #
    ############################################################################
    # 1. 生成目录, 目录名为sample_folder
    request = CreateFolderRequest(bucket, u'/sample_folder/')
    create_folder_ret = cos_client.create_folder(request)
    logger.info('create folder ret:' + str(create_folder_ret))

    # 2. 更新目录的biz_attr属性
    request = UpdateFolderRequest(bucket, u'/sample_folder/', u'这是一个测试目录')
    update_folder_ret = cos_client.update_folder(request)
    logger.info('update folder ret:' + str(update_folder_ret))

    # 3. 获取目录属性
    request = StatFolderRequest(bucket, u'/sample_folder/')
    stat_folder_ret = cos_client.stat_folder(request)
    logger.info("stat folder, return message: " + str(stat_folder_ret))

    # 4. list目录, 获取目录下的成员
    request = ListFolderRequest(bucket, u'/sample_folder/')
    list_folder_ret = cos_client.list_folder(request)
    logger.info("list folder, return message: " + str(list_folder_ret))
    # 5. 删除目录
    request = DelFolderRequest(bucket, u'/sample_folder/')
    delete_folder_ret = cos_client.del_folder(request)
    logger.info("delete folder, return message: " + str(delete_folder_ret))

if __name__ == '__main__':
    app_id = 1252034232               # 替换为用户的appid,整型
    secret_id = u'AKIDAAwWrzwZ2GKAnBIEtKVR6YkgMmxtF0B7'  # 替换为用户的secret_id，字符串型，必须加'u'表示unicode编码
    secret_key = u'pOmxtaIuJURAgy2s67uTowpTs41jBPPA'     # 替换为用户的secret_key，字符串型，必须加'u'表示unicode编码
    region = u"guangzhou" #           # 替换为用户的region，目前可以为 shanghai/guangzhou，字符串型，必须加'u'表示unicode编码

    # 生成客户端
    client = getClient(app_id, secret_id, secret_key, region)
    
    # 桶设置，如果桶不存在，则创建
    bucket = u'bucket2' # 设置桶名称，字符串型，必须加'u'表示Unicode编码
    
    #以下所有路径必须加'u'表示Unicode编码，否则无法通过
    # 上传小文件
    localPath = u"E:/develop/eclipse_python_php/workspace/PyPro1/cos-python-sdk-v4-master/setup.py"
    cosPath = u"/cos-python-sdk-v4-master/setup.py"
    uploadSimpleFile(bucket, client, localPath, cosPath)
    
    # 上传大文件
    localPath = u""
    cosPath = u""
#     uploadBigFile(bucket, client, localPath, cosPath)
    
    # 下载文件
    localPath = u""
    cosPath = u""
#     downloadFile(bucket, client, localPath, cosPath)