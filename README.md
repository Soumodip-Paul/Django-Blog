# Django-Blog 

Django-Blog is a blog application created using Python-Django framework.
It uses SQLite as database (default database by django).
It includes 2 factor authentication for logging into admin panel,
and PayTM Payment Gateway for payment purposes.
You can check demo here [Django-Blog](https://google.com).


## Run Locally

Clone the project

```bash
    git clone https://github.com/Soumodip-Paul/Django-Blog
```

Go to the project directory

```bash
    cd Django-Blog
```

Install dependencies

```bash
    pip install -r requirements.txt
```

Start the server

```bash
    cd blog
    python manage.py runserver
```


## Environment Variables

To run this project, you will need to add the following environment variables to your `./blog/blog/secret.py` file

```python
smtp_mail:str = "your email address"
smtp_pass:str = " Your Password "
site_name:str = "Your domain name for this website"
```


## License

[MIT License](https://choosealicense.com/licenses/mit/)

Copyright (c) 2022 [Soumodip Paul](https://github.com/Soumodip-Paul)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Feedback

If you have any feedback, please reach out to us at 
[Our Blog Website](https://spaul10032002.blogspot.com/p/contact-us.html)


## 🔗 Links
<!-- [![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://katherinempeterson.com/) -->
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/soumodip-paul-10032002)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/soumodippaul6)

