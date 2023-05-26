# DepEdit for CxG annotation

To apply a cascade of rules from a file like `cxn.ini` to a .conllu file with UD annotations using Python:

```
pip install depedit
python -m depedit -c cxn.ini infile.conllu
```

For documentation on writing DepEdit rule files see:

https://gucorpling.org/depedit/
