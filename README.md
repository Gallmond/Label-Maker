# Label Maker
Simple bespoke executable that builds barcoded .pdfs for printing as labels.

----

Friend of mine was telling me about a lengthy work task involving manually building barcodes using a browser tool, pasting them into a PDF maker, saving and printing using values from a product spreadsheet. Sounded like an easily automatable task and I wanted to play with python some more. Reduced tens of hours a work per month to tens of seconds.

Compiled into an executable for ease of use by non-techies with nuitka's 

`python -m nuitka --recurse-all --standalone labelmaker_source.py`

## Technologies used

- Python 3.6.2
    - xhtml2pdf 0.2.2
    - nuitka

## Launch

Simply run _labelmaker.exe_ in its dist folder which should contain:
```
somefolder/
├── labelmaker.exe
├── label_template.html
├── report.txt
├── input/
│   └── barcodes.csv
└── output/
```

Completed barcode pdfs will be saved to the output folder.

Output names were made to match the workflow already used (SKU name)