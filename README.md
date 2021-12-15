# DJANGO BLOG
This is a django blog created with bootstrap

Use the command to start project

```bash
pip install -r requirements.txt
```

and create a file in `./blog/blog/secret.py` file containing the following code

```python

smtp_mail:str = "your email address"
smtp_pass:str = " Your Password "

```

And change the following code in your `./blog/blog/settings.py` file for your custom email settings
```python

from .secret import smtp_mail,smtp_pass

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com' # your SMTP server host
EMAIL_PORT = 587 # smtp port ( 25 or 587 )
EMAIL_HOST_USER = smtp_mail
EMAIL_HOST_PASSWORD = smtp_pass

```