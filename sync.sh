mv *.png ./plotimages/
rsync -azP ./plotimages/ athena@athena.codes:~/AthenaWebsite/images/plots
