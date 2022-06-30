# tweet-profanity
Problem Statement:
Imagine there is a file full of Twitter tweets by various users and you are provided a set of words that indicates racial slurs. Write a program that can indicate the degree of profanity for each sentence in the file.

Assumptions
two files are provided such that one file contains tweets by various users and the other consists of a list of "profanity words".

The file containg tweets will be called as the "tweet file". It can have any one of the extensions - "txt/text/xls/xlsx/xlsm" and a following format: A single column containing the tweets preceeded by the users' Twitter handle. Can be with/without a header. For example,

"@User1 tweet"
"@user2 tweet"
"@user3 tweet"

The other file, called "search_words" file, contains a list of abusive words and/or racial slurs such that each "profinity word" is on a new line. This file must be a text file with extensions "txt/text".
Data used
For now I have used a temporary dataset I got from the internet to test the program.

Inputs taken
A file containing Twitter handles and their tweets such that each line contains one Twitter handle and tweets. Check any of the example files called "tweets" with extensions "txt/text/csv/xls/xlsx" for the correct format.
A "txt/text" file with one "profanity word" per line. Check the file called "search_words.txt" or "search_words.text" for the correct format.
Given these two files fulfilling the aforementioned requirements, the Python program identifies the degree of profanity per tweet. The degree of profanity is defined as the ratio of the number of abusive/racial words in a tweet to the total number of words in the times 100.

Outputs
A CSV file with 4 columns: User handles, original tweets, "profinity words", and degree of profanity - Check "tweets_analysis.csv".
