

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
- [No.5 Expand](https://github.com/blackmonkey121/verify#expand)
- [No.6 Docx](https://github.com/blackmonkey121/verify#docx)
- [No.7 License](https://github.com/blackmonkey121/verify#license)



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

**Download**  👉  [Click me **Download** verify-python](https://github.com/blackmonkey121/verify/archive/master.zip)

```shell
python setup.py instal   # 在 verify-python 根目录下执行
```



## Usage


###  VerifyGif

```python
from verify import VerifyGif

gif = VerifyGif()    # Get the instance of VerifyGif.
veri = gif('A48K')   # You can specify it yourself or generate it randomly.
veri.save_file()   # Save the verify code to `.Verify/verifyxxx.gif`
veri.get_binary()    # Get the verify code format binary.
```



###  VerifyPng

```python
from verify import VerifyPng

png_instance = VerifyPng()
veri = instance('J7Wd')
veri.get_binary()   # get
```



### Safe

Create encrypted all request parameters.

```python
from verify import Safe

s = Safe()

ret = s.coding(string='Mst4')
# ret : `IntcInN0clwiOiBcIkRcXHUwMG...XCJSU0FcIiwgXCJ2dFwiOiBcImdpZlwifSI=`

ret = s.parse(ret)
# ret : `{'str': 'Mst4', 'mtd': 'RSA', 'vt': 'gif'}`
```



### Config

> **way1** Use config file. This is recommended if there are many configuration information

```python
from verify import Config

# You can tell verify configuration information in the form of a file.
config = Config('my_conifg')/ config = Config('my_conifg.py')   # Extend name can be accept.
```

> **way2** Inherit the `Config` class, and then rewrite the attributes. This makes your code look clear, and you can add some methods. But it's a bit complicated.

```python
from verify import Config, VerifyGif

class MyConfig(Config):
    
    FRAME_NUMBER: int = 24
    VERIFY_SIZE: tuple = (40, 40)
    LINES_NUMBER: int = 4 

veri = VerifyGif(config=MyConfig)   # You must pass it as a parameter to VerifyGif/VerifyPng.
```

> **way3** Add attributes directly to `config`.  This is recommended if there is little configuration information.

```python
from verify import config

config.FRAME_NUMBER: int = 24
config.VERIFY_SIZE: tuple = (42, 42)
config.LINES_NUMBER: int = 5
```



### Cache

> This is a thread-safe cache. The package itself depends on it, which is convenient if you happen to need it in your project.  For example, save the generated verification code.

```python
from verify import Cache

cache = Cache(contain=1024, expiration=60 * 60)   
# contain: Maximum capacity.  expiration: timeout.

cache.set('key', 'value')   # set value.
cache.get('key')   # get value.
cache.clear()  # clear cache.
```

**tips:** You have to use your own instantiated object. 



## Example

### business server

> Create the `<img src="https://path/verify/verify_url_para">`

```python
from verify import Safe

s = Safe()
verify_url_para = s.coding('S7rE')
url = url + verify_url_para

# verify_url_para: IntcInN0clwsjMG...XCJSU0FcIiXCJ2dFwiOiBcImdpZlwifSI=
---------------------------------------------------
rander(<img src="https://path/verify/verify_url_para">)
render(<img src="https://xxx/verify/IntcInN0clwsjMG...XCJSU0FcIiXCJ2dFwiOiBcImdpZlwifSI=" alt="verify">)
```

### verify server 

> Get the verify_url_para, parse it. Create the verification code binary format.

```python
request_str = "IntcInN0clwsjMG...XCJSU0FcIiXCJ2dFwiOiBcImdpZlwifSI="
from verify import Safe, VerifyGif, VerifyPng

s = Safe()
request_data = s.parse(request_str)
# request_data: {'str': 'S7rE', 'mtd': 'RSA', 'vt': 'gif'}

verify_dict = {'gif': VerifyGif, 'png': VerifyPng}

def get_verify_binary(request_data):
    verify_type = request_data.get('vt', None)
    string = request_data.get('str', None)

    verify_cls = verify_dict.get(verify_type, None)

    if verify_cls is not None:
        instance = verify_cls()
        verify = instance(string=string)
        return verify.get_binary()
    else:
        raise Exception('Request parameter error.')

verify_binary = get_verify_binary(request_data)
return verify_binary   # Verification code in binary format.
```



## Expand



### Verify

> Provides support for two types of verification codes, namely **`GifVerify`** and **`PngVerify`**,
>
> When instantiating them, you can specify`Builder`、`config`、 `Filter`、`Storage`、`Style`.



- **Builder**
  - **_Create_char_**  create char image.
  - **_Create_background_**  create background layer.
  - **_back_fix_char_**  Mix character pictures into the background.
- **Filter**
  - **_char_filter_**   Will be called after `create_char` . 
  - **_back_filter_**  will be called after `create_background`.
  - **_frame_filer_**  will be called after `GifVerify/PngVerify.get_frame`

- **Storage**
  - **_save_file_**   Save the **GifVerify/PngVerify object** to the file system.
  - **_get_binary_**  Returns the binary data of this **GifVerify/PngVerify object**.
- **Style**
  - **_get_lines_** Location informations of interference line.
  - **_get_positions_**  Chareset position informations of in the background.
  - **_get_angles_**  Chareset angle informations of in the background.
  - **_frame_style_**  All style information of each layer.

> You can inherit them and rewrite them to meet your needs. For more detailed introduction, please see the [document]().



## Docx:



## License

### [GPLv 3.0](https://github.com/blackmonkey121/verify/blob/master/LICENSE) 

