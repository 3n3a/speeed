# SPEEED

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

**Download Data**

```bash
python3 download_parse.py -o <output-file> <url>
```

**Start API**

Serves the downloaded data

```bash
python3 -m fastapi run api.py
```