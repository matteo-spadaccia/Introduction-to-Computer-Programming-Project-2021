#GROUP: Maria Chiara Lischi, Gabriele Pacielli, Matteo Spadaccia

#SETUP
import pickle
import os

#TASK 1: DATA ACQUISITION and EVENTUAL CLEANING
default = input('Use dafault data paths? (y)(n) ')
while default != 'y' and default != 'n':
    default = input('Sorry: answer not recognized.\n\nUse dafault data paths? (y)(n) ')

#reloading request
if default == 'y':
    print('\nUsing default data paths,')
elif default == 'n':
    print('\nUsing custom data paths,\n\nInsert the preferred path in each of the following cases...')
    
#settings
if default == 'y':
    absolute_path = os.path.dirname(__file__)
    title_basics_path = os.path.join(absolute_path,'Inputs/title_basics.pkl')
    title_ratings_path = os.path.join(absolute_path, 'Inputs/title_ratings.pkl')
    title_principals_path = os.path.join(absolute_path, 'Inputs/title_principals.pkl')
    title_basics_cleaned_path = os.path.join(absolute_path, 'Inputs/title_basics_cleaned.pkl')
    title_ratings_cleaned_path = os.path.join(absolute_path, 'Inputs/title_ratings_cleaned.pkl')
    title_principals_cleaned_path = os.path.join(absolute_path, 'Inputs/title_principals_cleaned.pkl')
    most_voted_movie_path = os.path.join(absolute_path, 'Outputs/query1.pkl')
    top_10_path = os.path.join(absolute_path, 'Outputs/query2.pkl')
elif default == 'n':
    title_basics_path = input('Insert custom absolute path to title_basics.pkl: ')
    title_basics_cleaned_path = input('Insert desired absolute path to title_basics_cleaned.pkl: ')
    title_ratings_path = input('Insert custom absolute path to title_ratings.pkl: ')
    title_ratings_cleaned_path = input('Insert desired absolute path to title_ratings_cleaned.pkl: ')
    title_principals_path = input('Insert custom absolute path to title_principals.pkl: ')
    title_principals_cleaned_path = input('Insert desired absolute path to title_principals_cleaned.pkl: ')
    most_voted_movie_path = input('Insert desired absolute path to query1.pkl (most-voted movie): ')
    top_10_path = input('Insert desired absolute path to query2.pkl (top-10 prolific directors): ')
    
data_reloading = input('would you like to reload the data? (y)(n) ')
while data_reloading != 'y' and data_reloading != 'n':
    data_reloading = input('Sorry: answer not recognized.\n\nPlease, choose to reload the data or not: (y)(n) ')
    
#eventual reloading
if data_reloading == 'y':
    
    #Initializing
    print('\nOk, I will start from the raw data on your PC.\n\nReloading and cleaning data...')
     
    #reloading
    title_basics = pickle.load(open(title_basics_path,'rb'))
    title_ratings = pickle.load(open(title_ratings_path,'rb'))
    title_principals = pickle.load(open(title_principals_path,'rb'))

    #cleaning setup
    title_basics_cleaned = []
    title_ratings_cleaned = {}
    title_principals_cleaned = {}
    progress = 0
    progress_step = int(len(title_basics)/30)
    
    #cleaned data composition
    for movie in title_basics:
        flag = 0
        
        #basics test
        for datum in movie:
            if '\\N' in datum:
                flag = 1
                break
            
        #ratings test
        if flag == 0:
            code = movie[0]
            for datum in title_ratings[code]:
                if '\\N' in str(datum):
                    flag = 1
                    break
                
        #principals test        
        if flag == 0:
            for datum in title_principals[code]['director']:
                if '\\N' in datum:
                    flag = 1
                    break
        if flag == 0:
            for datum in title_principals[code]['cast']:
                if '\\N' in datum:
                    flag = 1
                    break
                
        #composition    
        if flag == 0:
            title_basics_cleaned.append([movie[0], movie [1], movie[2], int(movie[3]), movie[4], int(movie[5])])
            title_ratings_cleaned[code] = [int(title_ratings[code][0]),int(title_ratings[code][1])]
            title_principals_cleaned[code] = title_principals[code]
        
        #progress bar
        progress += 1
        if progress >= progress_step:
            progress = 0
            print('_', end = '')

    #confirmation
    print('\n\nReloading and acquisition completed:', len(title_basics_cleaned), 'movies considered.')
    
    #cleaned data storage
    pickle.dump(title_basics_cleaned, open(title_basics_cleaned_path,'wb'))
    pickle.dump(title_ratings_cleaned, open(title_ratings_cleaned_path,'wb'))
    pickle.dump(title_principals_cleaned, open(title_principals_cleaned_path,'wb'))

#eventual acquisition w/o reloading
else:
    
    #initialization
    print('\nOk, I will use the already cleaned data on your PC.\n\nAcquiring data...\n________', end = '')
    
    #acquisition
    title_basics_cleaned = pickle.load(open(title_basics_cleaned_path,'rb'))
    print('________', end = '')
    title_ratings_cleaned = pickle.load(open(title_ratings_cleaned_path,'rb'))
    print('________', end = '')
    title_principals_cleaned = pickle.load(open(title_principals_cleaned_path,'rb'))
    print('______', end = '')
    
    #confirmation
    print('\n\nAcquisition completed:', len(title_basics_cleaned), 'movies considered.')

#TASK 2-3: QUERIES
#request
query = 'vuoto'
while query != '0':
    query = input('What shall I do now? (0-exit)(1-most voted movie)(2-most prolific 20th century directors) ')
    while query != '0' and query != '1' and query != '2':
        query = input('Sorry: answer not recognized.\n\nPlease, choose a query: (0-exit)(1-most voted movie)(2-most prolific 20th century directors) ')    
    
    #QUERY 1: MOST VOTED MOVIE
    if query == '1':
        
        #setup
        print('\nOk, i will try the query 1.\n\nSearching...')
        maxVotes = 0
        maxMovie = 0
        tie = 0
        tie2 = 0
        progress = 0
        progress_step = int(len(title_ratings_cleaned.keys())/20)
        
        #code and votes number research
        for movie in title_ratings_cleaned.keys():
            if title_ratings_cleaned[movie][1] > maxVotes:
                maxMovie = movie
                maxVotes = title_ratings_cleaned[movie][1]
                maxRating = title_ratings_cleaned[movie][0]
                tie = 0
                tie2 = 0
            elif title_ratings_cleaned[movie][1] == maxVotes:
                tie += 1
                if title_ratings_cleaned[movie][0] > maxRating:
                    maxMovie = movie
                elif title_ratings_cleaned[movie][0] == maxRating:
                    tie2 += 1
                    
            #progress bar
            progress += 1
            if progress >= progress_step:
                progress = 0
                print('_', end = '')
        
        #title research
        for movie in title_basics_cleaned:
            if movie[0] == maxMovie:
                maxMovie = movie[2]
                #progress bar
                print('__________')
                break
        
        #confirmation
        if tie == 0:
            print('\nResearch completed: "', maxMovie, '" is the most rated movie, with ', maxVotes, ' votes.', sep = '')
        elif tie2 == 0:
            print('\nResearch completed: "', maxMovie, '" is the most rated movie, with ', maxVotes, ' votes.\nThere is a tie with other ', tie, ' films, but they have lower scores', sep = '')
        else:
            print('\nResearch completed: "', maxMovie, '" is one of the most rated movie, with ', maxVotes, ' votes.\nThere is a tie with other ', tie, ' films.', sep = '')
        
        #most voted movie eventual storage
        save = input('Shall I save this datum on your PC? (y)(n) ')
        while save != 'y' and save != 'n':
            save = input('Sorry: answer not recognized.\n\nPlease, choose to save the datum or not: (y)(n) ')    
        if save == 'y':
            pickle.dump([maxMovie, maxVotes], open(most_voted_movie_path,'wb'))
            print ('\nDone!')
        elif save == 'n':
            print('\nOk, nevermind.')
        
    #QUERY 2: MOST PROLIFIC DIRECTORS
    if query == '2':
        
        #setup
        print('\nOk, i will try the query 2.\n\nSearching...')
        title_directors_20 = {}
        top_10 = []
        tie = 0
        progress = 0
        progress_step = int(len(title_basics_cleaned)/20)
        
        #sorting 20th century data for director name
        for movie in title_basics_cleaned:
            if 2000 > movie[5] >= 1900:
                for name in title_principals_cleaned[movie[0]]['director']:
                    if name not in title_directors_20.keys():
                        title_directors_20[name] = 1
                    else:
                        title_directors_20[name] += 1
            
            #progress bar
            progress += 1
            if progress >= progress_step:
                progress = 0
                print('_', end = '')
        
        #selecting the most prolific directors
        for counter in range(10):
            moviesMax = 0
            nameMax = 0
            for name in title_directors_20.keys():
                if title_directors_20[name] > moviesMax:
                    moviesMax = title_directors_20[name]
                    nameMax = name
            top_10.append((nameMax, moviesMax))
            title_directors_20.pop(nameMax)
            
            #progress bar
            print('_', end = '')
            
        #eventual tie to n° 10 selection
        for name in title_directors_20.keys():
            if title_directors_20[name] == moviesMax:
                top_10.append((name, moviesMax))
        
        #confirmation
        print ("\n\nResearch completed: here is the most prolific directors' top 10 for 20th century...")
        
        #table settings
        nameLenMax = 0
        for director in top_10:
            if len(director[0]) > nameLenMax:
                nameLenMax = len(director[0])
        
        #table output
        print('  ', '_'*(16+nameLenMax), sep = '')
        print(' |__n_|_Movies_|_Name__', end = '')
        if nameLenMax >= 6:
            print('_'*(nameLenMax-5), '|', sep = '')
        else:
            print('|')
        tie = 0
        s = ' '
        for n in range(len(top_10)):
            
            #line setup
            if n != 0:
                if top_10[n][1] == top_10[n-1][1]:
                    tie += 1
                else:
                    tie = 0
            if n == len(top_10)-1:
                s = '_'
            
            #line output
            print(' |', s*(3-len(str(n+1-tie))), n+1-tie, s, '|', s*(1+int((7-len(str(top_10[n][1])))/2)), top_10[n][1], s*(int((7-len(str(top_10[n][1])))/2)), '|', s, top_10[n][0], s*(nameLenMax-len(top_10[n][0])), s, '|', sep = '')

        #top 10 eventual storage
        save = input('Shall I save these data on your PC? (y)(n) ')
        while save != 'y' and save != 'n':
            save = input('Sorry: answer not recognized.\n\nPlease, choose to save the data or not: (y)(n) ')    
        if save == 'y':
            pickle.dump(top_10, open(top_10_path,'wb'))
            print ('\nDone!')
        elif save == 'n':
            print('\nOk, nevermind.')

print('\nHope to have been useful, bye!')