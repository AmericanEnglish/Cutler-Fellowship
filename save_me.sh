# Pull down list of files
# Delete this failure if it's of the correct file extension
shopt -s nullglob
EXTENSION=$*
for f in *.$EXTENSION
do   
    echo "$f"
    rm "$f"
done
