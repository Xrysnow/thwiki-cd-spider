# -*- coding: gbk -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pyodbc
import os
import time

class MyPipeline(object):
    groups = []
    conn = None
    cursor = None
    drop_cmd = "DROP TABLE TRACKS;"
    creat_cmd =\
    '''CREATE TABLE TRACKS
    (ID       TEXT(255)    PRIMARY KEY,
    SOCIETY   TEXT(100)    NOT NULL,
    ALBUM     TEXT(100)    NOT NULL,
    IDX       TEXT(100)    NOT NULL,
    TITLE     TEXT(100), ARRANGE   TEXT(100),
    VOCAL     TEXT(100), LYRIC     TEXT(100),
    OGMUSIC   TEXT(255), SOURCE    TEXT(255),
    TTYPE     TEXT(25),  LENGTH    TEXT(10));'''
    insert_cmd =\
    '''INSERT INTO TRACKS (ID, SOCIETY, ALBUM, 
    IDX, TITLE, ARRANGE, VOCAL, LYRIC, OGMUSIC, 
    SOURCE, TTYPE, LENGTH) VALUES ('''

    def process_item(self, item, spider):
        for k in item:
            item[k]=item[k].replace("'","''")# in Access, two [single quote]s means [single quote]
        ic = self.insert_cmd+"'" + item['society'] + "-" + item['album'] + "-" + item['idx'] + "','"
        ic+=item['society'] + "','" + item['album'] + "','" + item['idx'] + "','" + item['title'] + "','"
        ic+=item['arrange'] + "','" + item['vocal'] + "','" + item['lyric'] + "','" + item['ogmusic'] + "','"
        ic+=item['source'] + "','" + item['ttype'] + "','" + item['length'] + "');"
        try:
            self.cursor.execute(ic)
            self.conn.commit()
        except Exception as e:
            for er in e.args:
                print(er.encode('utf-8').decode('gbk'))
        return item

    def open_spider(self, spider):
        path = os.path.dirname(os.path.realpath(__file__))
        file = path + r"\test.mdb"
        try:
            # 64bit, you need to install AccessDatabaseEngine_X64.exe
            self.conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" + file + ";")
            # 32bit
            # self.conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb)};Dbq=" + file + ";")
            self.cursor = self.conn.cursor()
            if self.cursor.tables(table='TRACKS').fetchone():
                self.cursor.execute(self.drop_cmd)
                self.conn.commit()
            self.cursor.execute(self.creat_cmd)
            self.conn.commit()
        except Exception as e:
            for er in e.args:
                print(er.encode('utf-8').decode('gbk'))

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
