# NLP01-Q&A Websites ANL
## Get data 

### 1、Using ZhiHu_C.py to get the searching results from ZhiHu.com

Example:

```python
#Import class file
import ZhiHu_C
#Import the necessary Python package
import os
import requests
from http.cookies import SimpleCookie
from fake_useragent import UserAgent
import random
import pandas as pd
import json
import brotli
import time
from pandas.io.json import json_normalize

#step1: Instantiate 
myZhiHu=Volume(['intel','i3'],r'C:\\Users\\jjsun\\Documents\\ZHIHU\\',5,['general','column'])
#step2: Instantiate intra-class functions CreatePath to create file paths
myZhiHu.CreatePath()
#step3: Instantiate ZhihuMain to save the crawled information
myZhiHu.ZhihuMain()
```
