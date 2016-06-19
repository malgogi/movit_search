import json, math
import numpy as np
import codecs
import re

#string format
#all none characters change '_'
def formattingStr( mystr ):
    return re.sub('[^a-zA-Z0-9]', '_', mystr );

movies = json.loads( open( '../data/formatted_docs.json' ).read() )
#print( items )
file_config = {
  'name' : "movie.n3",
};

n3File = "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n";
n3File += "@prefix owl: <http://www.w3.org/2002/07/owl#>.\n";
n3File += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n";
n3File += "@prefix log: <http://www.w3.org/2000/10/swap/log#>.\n";
n3File += "@prefix math: <http://www.w3.org/2000/10/swap/math#>.\n";
n3File += "@prefix list: <http://www.w3.org/2000/10/swap/list#>.\n";
n3File += "@prefix e: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#>.\n";
n3File += "@prefix prolog: <http://eulersharp.sourceforge.net/2003/03swap/prolog#>.\n";
n3File += "@prefix genres: <http://localhost:9000/n3/genres#>.\n";
n3File += "@prefix actors: <http://localhost:9000/n3/actors#>.\n";
n3File += "@prefix : <http://localhost:9000/n3/movies#>.\n\n";

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
    n3File += "#data\n";
    f.write( n3File )


    for idx, movie in enumerate( movies ):
        temp = ":";
        temp += formattingStr( movie[ "name" ] ) + "\n";
        temp += ":id " + str( idx ) + " ;\n";
        temp += ":name " + '"' + formattingStr( movie[ "name" ] ) + '"' + " ;\n";
        
        temp += ":actor ";
        if len( movie[ "actors" ] ) > 0 :
            for actor in movie[ "actors" ]:
                temp += 'actors:' + formattingStr( actor );
                temp += ", "; 
            #remove last ', '
            temp = temp[ : -2 ];
        else:
            temp += "actors:none";
        temp += ';\n';

        temp += ':genre ';
        if len( movie[ "genre" ] ) > 0 :
            for genre in movie[ "genre" ]:
                temp += 'genres:' + formattingStr( genre );
                temp += ", ";
            #remove last ', '
            temp = temp[ : -2 ];
        else:
            temp += "genres:none";
        temp += ';\n';

        temp += ":date " + movie["date"][-4:] + ".\n\n";
    
        f.write( temp );
    