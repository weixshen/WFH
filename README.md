# WordsFromHeadlines
    本应用自动从环球时报英文版抓取头版头条，分词后将所有单词列出，供用户进行记忆。单词记忆结束后，再去通读全文。对于不认识的生词，通过百度翻译的API可以看到中文解释。标记为认识的单词将不会再出现。

测试:
    
    # cd WFH/app
    # ./manage.py makemigrations
    # ./manage.py migrate
    # ./manage.py runserver
    浏览器中访问http://127.0.0.1/8000/wfh即可
