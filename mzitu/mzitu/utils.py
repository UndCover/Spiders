import platform

def downloadPath():
    if 'Windows' == platform.system():
        return 'D:/scrapy/Spiders/mzitu/mzitu/test/'
    else:
        return '/Users/UndCover/Desktop/Spider/Spiders/mzitu/test/'

DB_FILE='test.db'
DB_CREATE_TABLE_MAIN='''
    CREATE TABLE IF NOT EXISTS Information
    (ID             Text    PRIMARY KEY NOT NULL,
    -- 标题
    Title           Text	            NOT NULL,
    -- 生成的文件名
    FileName        Text                not null,
    -- 标记
    Tags            Text,
    -- 主链接
    Link            Text                NOT NULL,
    -- 日期
    PostDate        Text,
    -- 缩略图
    Thumb           Text,
    -- 图片数量
    PicCount        INT                 not null,
    -- 完成状态	0 未完成 1 完成 2 异常
    Done            INT                 not null
    );
'''
DB_CREATE_TABLE_CONTENT='''
    CREATE TABLE IF NOT EXISTS PicContent
    (ID             Text    PRIMARY KEY NOT NULL,
    -- 父级ID
    PID             Text                NOT Null,
    -- 连接
    link            Text                NOT NULL,
    -- 完成状态	0 未完成 1 完成
    Done            INT                 not null
    );
'''
DB_CREATE_TABLE_TAG='''
    CREATE TABLE IF NOT EXISTS Tag
    (ID             Text    PRIMARY KEY NOT NULL,
    TAG             Text    NOT NULL
    );
'''
