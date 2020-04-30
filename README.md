

<div align="center">
    <img src="https://github.com/blackmonkey121/verify/blob/master/image/verify_logo.png" alt="Verify-Logo">
</div>

# Verify ![](https://img.shields.io/badge/GPL-3.0-green)  ![](https://img.shields.io/badge/version-0.0.1-informational)  ![](https://img.shields.io/badge/python-3.x-blueviolet)
An elegant verification code generation framework.

## Contents

- [No.1 Background](https://github.com/blackmonkey121/verify#background)
- [No.2 Installation](https://github.com/blackmonkey121/verify#installation)
- [No.3 Usage](https://github.com/blackmonkey121/verify#usage)
- [No.4 Example](https://github.com/blackmonkey121/verify#example)
- [No.5](https://github.com/blackmonkey121/verify#)
- [No.5 License](https://github.com/blackmonkey121/verify#license)

## Background

Captchas are common in web development, but common captchas are easy to identify and bypass. The project provides a simple and flexible captcha generator that is efficient, secure, and easy to extend.



## Installation

### Way 1：

```pyhton
pip install verify-python
```


### Way 2：

```python
pip install git+git://github.com/blackmonkey121/verify.git
```

**or**

```python
pip install git+https//github.com/blackmonkey121/verify.git
```

### Way 3：

#### Download.  👉  [Click me **Download** verify-python](https://github.com/blackmonkey121/verify/archive/master.zip)

```shell
python setup.py instal   # 在 verify-python 根目录下执行
```



## Usage


####  VerifyGif

```python
from verify import VerifyGif

gif = VerifyGif()    # Get the instance of VerifyGif.
veri = gif('A48K')
veri.save_file()   # Save the verify code to `.Verify/verifyxxx.gif`
veri.get_binary()    # Get the verify code format binary.
```



####  VerifyPng

```python
from verify import VerifyPng

png_instance = VerifyPng()
veri = instance('J7Wd')
veri.get_binary()   # get
```



#### Safe


## PART 2 Detailed Configuration









## PART 3 ReWrite & Expand







# Docx:







