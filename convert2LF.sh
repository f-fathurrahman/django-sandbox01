# Remove \r or ^M
#sed -i 's/^M$//' "$1"
sed -i 's/^M//' *.py
