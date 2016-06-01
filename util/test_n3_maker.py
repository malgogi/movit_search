import json, math
import numpy as np
import codecs

movies = json.loads( open( '../data/formatted_docs.json' ).read() )
#print( items )
file_config = {
  'name' : "movie.n3",
};

n3File = "@prefix log: <http://www.w3.org/2000/10/swap/log#>.\n";
n3File += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n";
n3File += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n";
n3File += "@prefix : <http://www.agfa.com/w3c/euler/moives#>.\n\n";



    




#rule
#if user like movie, also like other movie
with codecs.open( file_config[ "name" ], 'w', encoding='utf8' ) as f:
    f.write( n3File )


    for movie in movies:
        temp = ""
        temp_name = ""
        for actor in movie[ "actors" ]:
            
            #movie directed by actor
            temp_name += movie[ "name" ].replace('/', '_');
            temp_name = temp_name.replace(':','');
            temp_name = temp_name.replace('!','');
            temp_name = temp_name.replace('#','');
            temp_name = temp_name.replace('&','');
            temp_name = temp_name.replace('*','');
            temp_name = temp_name.replace('.','');
            temp += ":" + temp_name.replace(' ', '_' ) + " :directed_by " + ":" + actor.replace( ' ', '_' ) + ".\n";
            #actors acting  movie
            temp += ":" + actor.replace( ' ', '_' ) + " :act " + ":" + temp_name.replace(' ', '_' ) + ".\n";

        f.write( temp );
    