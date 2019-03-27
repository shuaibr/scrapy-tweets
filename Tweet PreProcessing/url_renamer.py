import re 
  
def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url1 = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    
    url2 = re.findall('pic.twitter(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url1, url2
      
# Driver Code 
#string = "For further details go to  http:// Adele.com/live   pic.twitter.com/3lYaMe5pFJ"
string = 'My Profile: https://auth.geeksforgeeks.org / user / Chinmoy % 20Lenka / articles in the portal of http://www.geeksforgeeks.org/' 
print("Urls: ", Find(string)) 