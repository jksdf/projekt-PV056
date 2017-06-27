# IMDB graph learning
## Parsing
The here are the files that can be used to parse IMDB graph and are not meant to run on their own:
- ratingparser.py - used to parse rating file;
- actorparser.py - parses actor, actress and director files;
- genreparser.py - parses genres.
All of them use uncompressed files from the IMDB download list.
## Graph generation
Graph is generated using 'generategraph.py' script. This script outputs the graph to the output stream in a binary format (pickle). To see the input files passed as parameters, run the command without any parameters.
## Dataset preparation
File 'run.py' generate datasets used by Naive Bayes and SVM and 'run2.py' generates data for ANN. Running it without any parameter prints the requered parameters.
## Naive Bayes and SVM
To run Naive Bayes and an SVM, use 'learn.py' file. It uses matplotlib.pyplot to display all results in series.
## Apriori
Apriori generation is done using the 'gapriori.py' script. The output is sent to the output stream as a list of genre tuples where they each genre has either a 1 or 2 suffix to signify different movies (if both genres share the same suffix, they are in the same movie) and their support.
## Modules
igraph, apyori, matplotlib
## Examples
Generate dataset to predict movies from 2000 from movies in 1980 - 1999:
`./run.py actors.list actresses.list directors.list ratings.list genres.list 1980 2000 > dataset_1980_2000.json`
Use two such datasets for learning:
`./learn.py dataset_1970_1990.json dataset_1990_2010.json`
To use apriori algorithm:
`./gapriori.py actors.list actresses.list directors.list ratings.list genres.list 1980 2000 > results.json`
