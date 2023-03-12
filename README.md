![](intro.png)

# TonSDK - Python toolkit for [The Open Network](https://ton.org/docs)

[TonWeb JS](https://github.com/toncenter/tonweb) inspired library. \
Forked from [tonfactory/tonsdk](https://github.com/tonfactory/tonsdk/).


# Install

```
$ pip install git+https://github.com/devdaoteam/tonsdk
```


# Getting started

An example of doing an elementary thing - converting an address from the
raw form to human readable.
```python
>>> from tonsdk.utils import Address
>>> a = Address("0:21137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D8998270")
>>> a.to_string(True, True, True)
'EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT'
```


## Next
- [**More usage examples**](examples/)
- [**Get Toncenter API key**](https://t.me/tonapibot)
- [**Explore the code**](tonsdk/)
