# mp-dep
Counter of partially independent &amp; fully embedded structures for Master Project

## Input format
rsd

## Usage
Linux commands to call the counter and store the results with headings:

```
echo "directory,partially independent structure,fully embedded structure" > subpattern.csv
find PATH_TO_YOUR_DOCUMENTS/* -type d | xargs python3 subpattern.py >> subpattern.csv
```
