from mnemonic import Mnemonic
import bip32utils
import requests
import sys
import random
import re

mnemo = Mnemonic("english")

target=[
['xxxx'], # word on plate is "like"  ???
['muscle'], # word on plate is "love"  ???
['xxxx'], # word is "king"
['shaft'], # word is "place"
['task'], # word on plate is "closet"    ???
['xxxx'], # word on plate is "repel"
['nut'], # word on plate is "pear"
['xxxx'], # word on plate is "lizard" ???
['fault'],  # word on plate is covered up
['list'], # word on plate is "fast"
['xxxx'], # word on plate is "fast"
['excess'], # word on plate is "fast"
]

allwords=[]
for line in open('bip39.txt'):
  allwords.append(line.strip()) 

target[0]=allwords
target[2]=allwords
target[5]=list(filter(re.compile('^p').match, allwords))
target[7]=list(filter(re.compile('^[pygjq].{4,}').match, allwords))
target[10]=list(filter(re.compile('^[fhiklmnrvwx]').match, allwords))

keyspace = 1
print(len(target))
for i in range(0,len(target)):
  keyspace *= len(target[i]) 

print ("keyspace size is %i (%i bits)" % (keyspace, len(bin(keyspace))-2))

starting = random.randint(0,keyspace)
#starting = 0 # for when you're all alone

for x in range(starting,keyspace): # know your limits
  mystring=""
  eol=0

  if x%10000 == 0:
    sys.stderr.write(str('{:3.10f}'.format(x/keyspace*100))+"% complete\n")
    #sys.stderr.write("keyspace size is %i (%i bits)\n" % (keyspace, len(bin(keyspace))-2))

    sys.stderr.flush()
  
  remaining=x
  for word in range(0,len(target)):
    choice = int(remaining%len(target[word]))
    mystring+=target[word][choice]+' '

    if(choice == len(target[word])-1 ): # okay, we're at the end of this word placement
      eol+=1

    remaining=remaining/len(target[word])
   
  # uncomment for debug to ensure proper mnemo
  # print(mystring.strip())

  try:
    win = mnemo.check(mystring.strip())
    if win:
      print(mystring) # print the winnings
      seed = mnemo.to_seed(mystring.strip(),"")
      bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)

      # standard derivation path m/44'/0'/0'/0
      bip32_child_key_obj = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
      address = bip32_child_key_obj.Address()
      privkey = bip32_child_key_obj.WalletImportFormat()
      # print out public address
      print(address)

      # print out private key in format that can be loaded in wallets
      print(privkey)

      # see if this address has ever recieved coins
      #print(requests.get('https://blockchain.info/q/getreceivedbyaddress/'+address).text)
  except Exception as e:
    print("nope "+str(e))

  if(eol==len(target)): # if we've reached the end of every line, we're done
    break
