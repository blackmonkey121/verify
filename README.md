

<div align="center">
    <img src="https://github.com/blackmonkey121/verify/blob/master/image/verify_logo.png" alt="Verify-Logo">
</div>

# Verify ![](https://img.shields.io/badge/GPL-3.0-green)  ![](https://img.shields.io/badge/version-0.0.2-informational)  ![](https://img.shields.io/badge/python-3.x-blueviolet)
An elegant verification code generation framework.

## Contents

- [No.1 Background](https://github.com/blackmonkey121/verify#background)
- [No.2 Installation](https://github.com/blackmonkey121/verify#installation)
- [No.3 Usage](https://github.com/blackmonkey121/verify#usage)
- [No.4 Example](https://github.com/blackmonkey121/verify#example)
- [No.5 Expand&Overwrite](https://github.com/blackmonkey121/verify#expand--overwrite)
- [No.6 Configuration table](https://github.com/blackmonkey121/verify#configuration-table)
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
python setup.py install   #  verify-python root directory.
```



## Usage


###  VerifyGif

```python
from verify import VerifyGif

gif_instance = VerifyGif()    # Get the instance of VerifyGif.
veri = gif_instance('A48K')   # You can specify it yourself or generate it randomly.
veri.save_file()   # Save the verify code to `.Verify/verifyxxx.gif`
veri.get_binary()    # Get the verify code format binary.
```



###  VerifyPng

```python
from verify import VerifyPng

png_instance = VerifyPng()
veri = png_instance('J7Wd')
veri.get_binary()
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

> **Tips** Automatically call your "_clean" ending method. Special treatment has been made to the single example. You can also use it as a normal class, and add methods to the config object at any time.

```python
from verify import Config

class MyConfig(Config):

    def size_clean(self):
        """ Will be called immediately upon instantiation . """
        self.bar()

        x, y = self.VERIFY_SIZE
        x = x if x <= 180 else 180
        y = y if y <= 50 else 50
        self.VERIFY_SIZE = (x, y)

    def bar(self):
        """ The method will bound the signal object config ."""
        print('hello config')
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

render(<img src="https://path/verify/verify_url_para">)
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

**[More examples]()**

## Expand & Overwrite

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

### Storage

```python
from verify import VerifyPng, PngStorage


class MyStorage(PngStorage):

    def show_img(self):

        from PIL import Image

        img = Image.open(self.instance)   # Read image from self.instance

        img.show()  # show the image.


veri = VerifyPng(storage=MyStorage)   # Instantiate VerifyPng

png = veri('HQ3r')  # Return `MyStorage` instance.

png.show_img()   # Call `show_img` methods.
```



### Filter

```python
from verify import VerifyPng, PngFilter


class MyFilter(PngFilter):

    def char_filter(self, verify: object, char: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        ...
        print('Overwrite char_filter. ')
        ...
        return super().char_filter(verify=verify, char=char, *args, **kwargs)


veri = VerifyPng(filter=MyFilter)
png = veri('HQ3r')
```



### Builder

```python
from verify import VerifyPng, PngFrameBuilder


class MyBuilder(PngFrameBuilder):

    def create_background(self, back_filter, *args, **kwargs) -> 'Image.Image':
        ...
        print('Overwrite create_background. ')
        ...
        return super().create_background(back_filter=back_filter, *args, **kwargs)


veri = VerifyPng(builder=MyBuilder)
png = veri('HQ3r')
```



### Style

```python
from verify import VerifyPng, PngStyle


class MyStyle(PngStyle):
    
    def get_angles(self, *args, **kwargs) -> 'Iterable':
        ...
        print('Overwrite get_angles. ')
        ...
        return super(MyStyle, self).get_angles()


veri = VerifyPng(style=MyStyle)
png = veri('HQ3r')
```



### Config

> Config will provide a hook that will call all methods ending in `_clean`. This can dynamically adjust the parameters, especially when the values of other parameters are not clear. You can also filter and add specific parameters.

```python
from verify import VerifyPng, Config


class MyConfig(Config):

    VERIFY_SIZE = (200, 54)   			# Write custom configuration information
    VERIFY_CODE_NUMBER = 6					# it will be used first.
    VERIFY_CODE_SIZE = (50, 50)
    DEFORM_OFFSET = 6
    DEFORM_NUMBER = 2	

    # Methods ending in `_clean` will be called by default.
    def deform_clean(self):
        self.DEFORM_NUMBER = 1 if self.DEFORM_NUMBER < 1 else self.DEFORM_NUMBER

veri = VerifyPng(storage=MyStorage, config=MyConfig)

png = veri()
png.show()
```

> Some adjustments have been made to the singleton object, allowing arbitrary methods to be implemented in the custom class, and these methods will be added to the configuration object dynamically, and you can call them anywhere.

```python
class MyConfig(Config):
    VERIFY_SIZE = (200, 54)

    # Methods ending in `_clean` will be called by default.
    def para_clean(self):
        self.DEFORM_NUMBER = 1 if self.DEFORM_NUMBER < 1 else self.DEFORM_NUMBER
        self.check_circle_number()
        self.check_deform_number()

    def check_circle_number(self, default=4):
        self.CIRCLE_NUMBER = self.CIRCLE_NUMBER if 2 < self.CIRCLE_NUMBER < 6 else default

    def check_deform_number(self, default=2):
        self.DEFORM_NUMBER = self.DEFORM_NUMBER if 0 < self.DEFORM_NUMBER <= 2 else default

```



### end

> You can pass in multiple custom classes at the same time, as long as they follow the corresponding interface.

```python
...
veri = VerifyPng(storage=MyStorage, config=MyConfig, filter=MyFilter, builder=MyBuilder, style=MyStyle)

png = veri('H7rJ')
png.show()
...
```

> Follow the interface without inheriting the default class. All interfaces are aggregated in `verify.abc.py`  .
>
> **Interface list**: `AbstractVerify`,` AbstractFilter`,` AbstractStyle`, `AbstractStorage`,` AbstractFrameBuilder`

```python
from verify.abc import AbstractFilter


class MyFilter(AbstractFilter):

    def back_filter(self, verify: object, back: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        return back

    def frame_filter(self, verify: object, *args, **kwargs) -> 'Image.Image':
        return verify.frame

    def char_filter(self, verify: object, char: 'Image.Image', *args, **kwargs) -> 'Image.Image':
        return char


veri = VerifyPng(filter=MyFilter, storage=MyStorage)
png = veri('Ag3r')
png.show()
```



## Configuration table

| Configuration |Default|Meaning |
| ------------- | ------- | ------- |
| VERIFY_CODE_SET | NUMBERS + CHARS_BIG + CHARS_LOW <  list > |Random character set|
|CHAR_FONT|ImageFont.truetype('Arial.ttf', 40)| Font and size                      |
|VERIFY_CODE_NUMBER|4|Number of characters on each layer|
|VERIFY_CODE_SIZE|(40, 40)  < pixel >|Character size|
|BACK_COLOR|(255, 255, 255, 255)  < pixel >|Background color|
|CHAR_COLOR|(0, 0, 0, 255)  < pixel >|Character color|
|NULL_COLOR|(0, 0, 0, 0)  < pixel >|Null color|
|VERIFY_SIZE|(180, 60)  < pixel >|CAPTCHA size|
|BACK_NOISE_NUMBER|200|Number of background noise|
|BACK_NOISE_TYPE|2  < pixel >|Size of background noise|
|LINES_NUMBER|4|Number of interference lines|
|CHAR_CUT_NUMBER|8|Number of character fragments|
|CHAR_CUT_PRESENT|0.2|Size of incomplete area|
|CIRCLE_NUMBER|6|Number of interference circle|
|FRAME_NUMBER|30|Frame number of GIF Verify|
|TRACK_INTERVAL|10 < pixel >|Character rotation radius|
|ANGLE_INTERVAL|60 < ±60 >|Rotation range of characters|
|RSA_FOLDER|RSA_KEY|RSA key save directory|
|RSA_KEY_DIR|`verify.RSA_KEY` < builder-in path >|RSA key save path|
|SAFE_ENGINE|'RSA'|Default encryption engine|
|SECRET_KEY|'a-=3bb51t_x#........s4_=w^40xj#7g'|Secret key for fast encryption engine|
|STORAGE_DIR|'Verify'|Save location of CAPTCHA|
|DEFORM_NUMBER|2|Number of character twists|
|DEFORM_OFFSET|6 < pixel >|The degree of character distortion|




## License

### [GPLv 3.0](https://github.com/blackmonkey121/verify/blob/master/LICENSE) 

