# mp-dep
Counter of partially independent &amp; fully embedded structures in this MP

Linux commands to call the counter and store the results with headings:

echo "directory,partially independenty structure,fully embedded structure" > subpattern.csv

find PATH_TO_YOUR_DOCUMENTS/* -type d | xargs python3 subpattern.py >> subpattern.csv 
