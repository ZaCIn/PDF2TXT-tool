# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 08:18:33 2018

@author: ZJ
"""

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def parsePDFtoTXT(filename):
    fp = open(filename, 'rb')#以二进制模式打开
    #用文件对象来创建一个pdf文档解析器
    parser = PDFParser(fp)
    #创建一个PDF文档
    doc = PDFDocument()
    #连接解析器和文档
    parser.set_document(doc)
    doc.set_parser(parser)
    #提供初始密码
    #如果没有密码，就创建一个空字符串
    doc.initialize()
    #检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF资源管理器来管理共享资源
        rsrcmgr = PDFResourceManager()
        #创建PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        #创建PDF解释器
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        #循环遍历列表，每次处理一个page内容
        for page in doc.get_pages():     #doc.get_pages() 获取page列表
            interpreter.process_page(page)
            #接受该页面的LTPage对象
            layout = device.get_result()
            '''这里layout是一个LTPage对象，里面存放着这个page解析出的各种对象，
            一般包括LTTextBox, LTFImage,LTFigure,LTTextBoxHorizontal等,想要
            获取文本就获得对象的text属性'''
            for x in layout:
                if (isinstance(x,LTTextBoxHorizontal)):
                    text = x.get_text()   #获取文本内容
                    print(text)
                    with open('text.txt','a',encoding="utf-8") as f:                        
                        f.write(text)
                        
    fp.close()
    

if __name__ == '__main__':
    parsePDFtoTXT('test.pdf ')
                    
            
