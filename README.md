# thwiki-cd-spider
This code can fetch CD infomation from [this page](http://thwiki.cc/%E5%90%8C%E4%BA%BA%E7%A4%BE%E5%9B%A2%E5%88%97%E8%A1%A8) at [thwiki.cc](http://thwiki.cc). The result will be stored in a Microsoft Access Database file so that it can be used in other places (such as foobar2000).

## Environment
- windows
- python 3.5
- scrapy
- pyodbc

## Usage
- Double click `run.bat` and wait, you will get `test.mdb` in `scrapyspider` folder.

## Note
- This code is windows only since it need Microsoft Access Driver. You will need to modify `pipelines.py` on other platforms.
- You need to install AccessDatabaseEngine_X64.exe if your windows is 64-bit. You can get it from [here](https://www.microsoft.com/en-us/download/details.aspx?id=13255).
- This code is written in Feb. 2017 and haven't updated. If it's broken, just raise an issue.
