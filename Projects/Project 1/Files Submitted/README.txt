I used [tinydb] for a database implementation.

Local Setup is as follows:
1. Open the directory you have the project saved. On iLab machines make sure to
first run export PATH="$PATH:/koko/system/anaconda/bin"
2. Activate a python 3 environment by running `source activate python38`.
3. pip3 install --user -r requirements.txt

shell script:
python auth.py AddUser <user> <password>
python auth.py Authenticate <user> <password>
python auth.py SetDomain <user> <domain>
python auth.py DomainInfo <domain>
python auth.py SetType <object> <type>
python auth.py TypeInfo <type>
python auth.py AddAccess <operation> <domain> <type>
python auth.py CanAccess <operation> <user> <object>
python auth.py Clear

The Clear command will clear the database.

Sample Test Script
$ python auth.py AddUser ryan coslove
Success
$ python auth.py AddUser ryan coslove
Error: user exists
$ python auth.py AddUser allen richard
Success
$ python auth.py Authenticate ryan coslove
Success
$ python auth.py Authenticate allen coslove
Error: bad password
$ python auth.py Authenticate john coslove
Error: no such user
$ python auth.py SetDomain ryan coach
Success
$ python auth.py SetDomain allen player
Success
$ python auth.py DomainInfo coach
ryan
$ python auth.py DomainInfo player
allen
$ python auth.py SetType word position
Success
$ python auth.py SetType schedule time
Success
$ python auth.py TypeInfo position
word
$ python auth.py TypeInfo time
schedule
$ python auth.py AddAccess write player position
Success
$ python auth.py AddAccess write coach time
Success
$ python auth.py CanAccess write ryan word
Error: access denied
$python auth.py CanAccess write allen word
Success
$ python auth.py CanAccess write ryan schedule
Success
$ python auth.py CanAccess write allen schedule
Error: access denied

There is a database file saved called db.json. The results with the above script were:
{
"users": {
  "1": {
    "username": "ryan",
    "password": "coslove",
    "domains": ["coach"]
    },
  "2": {
    "username": "allen",
    "password": "richard",
    "domains": ["player"]
      }
    },
    "objects": {
      "1": {
      "name": "word",
      "types": ["position"]
      },
      "2": {
      "name": "schedule",
      "types": ["time"]
        }
      },
      "access": {
        "1": {
        "operation": "write",
        "domain": "player",
        "type": "position"
        },
        "2": {
        "operation": "write",
        "domain": "coach",
        "type": "time"
        }
      }
  }
