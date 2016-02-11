#!/bin/bash

if [ ! -d "./plotimages/$*" ];
then
    mkdir "./plotimages/$*/"
fi
mv *.png "./plotimages/$*"
rsync -azP "./plotimages/" athena@athena.codes:~/AthenaWebsite/images/plots
