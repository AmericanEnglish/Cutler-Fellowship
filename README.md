# Cutler Fellowship

This project revolved around a scholarship given to me by Olivet College which was donated by David Cutler. In acceptance of the scholarship the recepient is required to contribute something to Mathematics or Computer Science.

# My Contribution
## Project
My goal is provide an open-course tool that will load in files generated by the website [url here]. Then it spit out graphs with the option to smooth the data from a variety of options

## Requirements
### For data processing
* [NumPy](http://www.numpy.org/)
* [matplotlib](http://matplotlib.org/)

### For database integration
* [SQLite3](https://www.sqlite.org/)
* [PostgreSQL](http://www.postgresql.org/)
  * [psycopg2](http://initd.org/psycopg/)

### Gui Drawing
* [Kivy](https://Kivy.org)

### Relational Model for Data
* [Quick Schema PDF](http://athena.codes/images/relationmodel.pdf)
 * Underlined values are Primary Keys. FK dependants are referenced in the next column
 * It is worth noting that this may change quick a bit, check back.
* [ER Diagram](http://athena.codes/images/erdia.png)

### First Gui Draft Designs
* [Main Window](http://athena.codes/images/Sample.1.MainWindow.png)
* [Detected New Files](http://athena.codes/images/Sample.1.Detected.png)
 * For when the program detects files that haven't been input into the database
* [A little plot](http://athena.codes/images/Sample.1.PlotWindow.png)

## Documentation of Testing
* Seems that into_db works and successfully puts kepler data into both an PostgreSQL and a SQLite3 database. This means that I can now work on other things. Although there are some things that should be improved in this realm:
 1. Fix the generate_tables.sql NUMERIC criteria to be better suited for the data. Not just NUMERIC(30,15). Not all values require this much significance.
 2. Run tests on the above statement and test for the insertion of 10 files. (very time consuming on a laptop)
  * The output text in [full](http://athena.codes/ftp/output.intodb.01232016.txt)
 3. implement hashing. Filenames can be changed for tons of reasons. hash the file CONTENTS and use those as a UID instead of filenames. **Wishlist**
* The function is now plotting. Now time to try and make some sense of the messy data! Just look at this graph of [cadence number vs sap_flux](http://athena.codes/images/plot1)
* I've now added flag functionality. This program should use the flag and arguments to effectively decide what is supposed to happen. This way i don't have to constantly change the name/main statement at the end. Check the sample! [flag plotting](http://athena.codes/ftp/flaglog.txt)
 * Need to add flag debugs. If you enter a flag but not an item after it, this can cause trace errors.
* Polyfit was actually very very easy to implmenet. Numpy added a function to even deal with the coefficient so that it's a simple plug and play or creating a new array from old data. This, as i thought it would, has increased the ease of coding. Next stop: checking how the correction works on the quarterly data. Then DATA SMOOTHING! 
* Plots are now viewable. I've written a script that will update my remote webserver. Simply going to http://athena.codes/images/plots will allows you to view all the generated plots. Some of these will most likely be debugging plots but they will all be timestamped.
* It looks like the straightening suggestion has worked. The graph seems to simulate a regular wave. I've decreased the point size and quadrupled the size of the image. Check [it](http://athena.codes/images/plots/plot2016-02-04-10:22:47.300087.stitched.png)