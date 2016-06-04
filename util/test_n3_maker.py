import json, math
import numpy as np
import codecs
import re

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
# with codecs.open( file_config[ "name" ], 'w', encoding='utf8' ) as f:
#     f.write( n3File )


#     for movie in movies:
#         temp = ""
#         temp_name = re.sub('[^a-zA-Z0-9]', '_', movie[ "name" ]);

#         #actor rule
#         for actor in movie[ "actors" ]:
#             temp_actor = re.sub('[^a-zA-Z0-9]', '_', actor );
#             temp += ":" + temp_name + " :directed_by " + ":" + temp_actor + ".\n";
#             #actors acting  movie
#             temp += ":" + temp_actor + " :act " + ":" + temp_name + ".\n";

#         #date rule
#         temp += ":" + temp_name + " :date " + ":" + movie["date"][-4:] + ".\n";
        
#         #genre rule
#         for genre in movie["genre"]:
#             temp += ":" + temp_name + " :genre " + ":" +re.sub('[^a-zA-Z0-9]', '_', genre) + ".\n";
        
#         f.write( temp );

with codecs.open( file_config[ "name" ], 'w', encoding='utf8' ) as f:
    f.write( n3File )


    for movie in movies:
        temp = "["
        movie_name = re.sub('[^a-zA-Z0-9]', '_', movie[ "name" ]);

        #actor rule
        for actor in movie[ "actors" ]:
            temp_actor = re.sub('[^a-zA-Z0-9]', '_', actor );
            temp += ":" + temp_name + " :directed_by " + ":" + temp_actor + ".\n";
            #actors acting  movie
            temp += ":" + temp_actor + " :act " + ":" + temp_name + ".\n";

        #date rule
        temp += ":" + temp_name + " :date " + ":" + movie["date"][-4:] + ".\n";
        
        #genre rule
        for genre in movie["genre"]:
            temp += ":" + temp_name + " :genre " + ":" +re.sub('[^a-zA-Z0-9]', '_', genre) + ".\n";
        
        f.write( temp );