# Suzuki Kasami Implementation using Python 

## Introduction
   The program stored in programsuzukikasami.py file is implementation of Suzuki Kasami Algorithm in Python.
   
## Pre-Requisites

1. Install python 3.x and name the python executable file as `python3`
2. Script is assuming python installation location as `/usr/local/bin` . If your python installation location is different,
please change the path in the shebang (mentioned in the first line of code)


## Usage
  # Inputs required to run the script
a. Site Count(`-c count`): Number of sites in distributed system. Note that site id numbering starts from 0. So, if site count is
               6, then site ids are  0,1,2,3,4,5

b. Site with token(`-t number`): Site id for the site which currently has the token

c. Supply `--exec` as third argument to denote that site having token is executing the critical section. 
Supply `--no-exec` as third argument to denote site having token is not executing critical section (idle)

  # Examples
1. Run the script with 5 sites and site with id 2 having the token and executing critical section, using command below:
    ```
   python3 programsuzukikasami.py -c 5 -t 2 --exec
   ```
2. Run the script with 4 sites and site with id 2 having the token and not executing critical section, using command below:
    ```
   python3 programsuzukikasami.py -c 4 -t 2 --no-exec
   ```
  # Inputs needed during script runtime

1. Type of Message ==> Has to be one of REL, REQ, OVER.
  Mention REL if you want the site ID holding the token to release Critical Section
  Mention REQ if you want a particular site to request for token
  Mention OVER to exit the script

2. Site ID ==> Mention the ID of the Site against which you want to operate the Type of message (REQ/REL) as mentioned in Point 1.
