import re, os, sys, platform
import pandas as pd
import openpyxl
from platform import python_version


tweet_file_name = input("give name of the tweet file: ")
print()
abuses_file_name = input("give name of the search (abuses) file: ")
print()

def get_file_path(file_name): 
    pwd = os.getcwd()
    abs_file_path = [] 
    for root, dir, files in os.walk(pwd):
        if file_name in files:
            abs_file_path.append(os.path.join(root, file_name))
    return abs_file_path[0]

def get_input_file(header, file_path, file_ext):    
    header = header.lower()
    if header == 'y':
        header_option = "infer"
    else: 
        header_option = None    
    if file_ext in ["txt", "text", "csv"]: 
        input_file = pd.read_csv(file_path, header=header_option, \
            delimiter="\n")
    elif file_ext == "xls": 
        input_file = pd.read_excel(file_path, header=header_option)
    else: 
        input_file = pd.read_excel(tweet_file_path, header=header_option, \
                    engine="openpyxl")
    return input_file

tweet_file_path = get_file_path(tweet_file_name)
abuses_file_path = get_file_path(abuses_file_name)
print("path of the tweet file: %s" %(tweet_file_path))
print()
print("path of the search (abuses) file: %s" %(abuses_file_path))
print()

if not os.path.isfile(tweet_file_path): 
    print("path of tweet file incorrect - check file path and try again!")
elif not os.path.isfile(abuses_file_path): 
    print("path of search (abuses) file incorrect - check file path and try again!")
    sys.exit()
else: 
    if abuses_file_path.split("\\")[-1].split(".")[-1] not in ['txt', "text"]: 
        print("file with abuses/racial slurs must be a text file with extension txt/text - create file with correct extension and try again")
        sys.exit() 
    else: 
        if os.stat(abuses_file_path).st_size > 0:
            with open(abuses_file_path, "r") as f_bad_words:
                list_of_abuses = []
                for line in f_bad_words: 
                    line = line.strip("\n")
                    list_of_abuses.append(line)
    
    if os.stat(tweet_file_path).st_size > 0: 
        tweet_file_ext = tweet_file_path.split("\\")[-1].split(".")[-1]     
        allowed_extensions = ["txt", "csv", "xls", "xlsm", "xlsx"]
        if tweet_file_ext not in allowed_extensions: 
            print(f'input file extension is not allowed - allowed extensions:, {allowed_extensions} \n')
            print("convert file to allowed extension only and try again!")
            print()
            sys.exit() 
        else:
            file_header_option = input("does the tweet file has any header? [y/n] ")
            print()
            input_file = get_input_file(file_header_option, tweet_file_path, tweet_file_ext)
                
        num_cols = input_file.shape[1]
        old_col0 = input_file.columns.to_list()[0]
        input_file = input_file.rename(columns={old_col0: "Tweets"})  
      
        print("first 3 lines of the input file:")        
        print(input_file.head(3))
        print()
        print("tweet file has %d rows and %d columns" %(input_file.shape[0], input_file.shape[1]))
    
        input_file["User"] = input_file["Tweets"].apply(lambda x: [x for x \
            in x.split(" ") if x.startswith("@")][0])
        input_file["User"] = input_file["User"].apply(lambda x: str(x)) 
    
        input_file["Tweets"] = input_file["Tweets"].apply(lambda x: [x for x \
            in x.split(" ") ][1:])
        input_file["Tweets"] = input_file["Tweets"].apply(lambda x: " ".join(x))
    
                                   
        def search_foul_words(x):     
            tmp_list = []
            for y in list_of_abuses: 
                if re.search(y, x, re.IGNORECASE) is not None:   
                    tmp_list.append(y) 
                else: 
                    pass 
            another_tmp_list = []
            for item in tmp_list: 
                if len(item) == 0:
                    pass 
                else:
                    another_tmp_list.append(item)
            
            foul_words = ", ".join(another_tmp_list)
            return foul_words            
                                   
        input_file["Foul Words"] = input_file["Tweets"].apply(search_foul_words)
        input_file.insert(0, "User Handle", input_file["User"].values)
        input_file = input_file.drop(["User"], axis=1)
        
        input_file["Num. Foul Words"] = input_file["Foul Words"].apply(\
            lambda x: len(re.findall(r'\w+', x)))      
    
        input_file['Total Word Count'] = input_file['Tweets'].apply(lambda x: \
            len(re.findall(r'\w+', x)))
        
        input_file["Deg. Profanity"] = input_file["Num. Foul Words"]/input_file["Total Word Count"]
    
        print("final output after analysis:") 
        print(input_file) 
        print() 
        
        input_file.to_csv("tweets_analysis.csv", index=False)
