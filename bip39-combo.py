from mnemonic import Mnemonic
import bip32utils
import requests

mnemo = Mnemonic("english")

# example trying to crack 
# https://www.reddit.com/r/whatisthisthing/comments/i63122/a_metal_plate_with_random_words_engraved_found/
# using the "opposite words" method.
# since some bip39 words aren't real, but their opposites seem to be

target=[
['differ'], # word on plate is "like"  ???
['despair', 'abandon'], # word on plate is "love"  ???
['peasant'], # word is "king"
['remove'], # word is "place"
['desk','room'], # word on plate is "closet"    ???
['attract'], # word on plate is "repel"
['apple'], # word on plate is "pear"
['mouse'], # word on plate is "lizard" ???
['slow'], # word on plate is "fast"
['person','snake'], # word on plate is "angel"  ??
['found'], # word on plate is "lost"
['circle'], # oppisite of "line"
['please'], # word on plate is "hurt"
['rude'], # word on plate is "culture"  ??
['rare'], # word on plate is "trope"
['total'], # word on plate is "section"
['false'], # word on plate is "true"
['follow'], # word on plate is "lead"
['admit'], # word on plate is "suggest"  ?????
['win'], # word on plate is "loose", maybe misspelling of lose?
['cheese'], # word on the plate is "wine"
['breeze','lazy'], # word on plate is "laber"  ????????????
['local'], # word on plate is "global"
['myth']  # word on plate is covered up
]

allwords=[]
for line in open('bip39.txt'):
  allwords.append(line.strip()) 

#target[13]=allwords
#target[19]=allwords
target[23]=allwords # use every possible bip39 word for this slot

for x in range(0,5000000000): # know your limits
  mystring=""
  eol=0
  
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
      #print(mystring) # print the winnings
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
      print(requests.get('https://blockchain.info/q/getreceivedbyaddress/'+address).text)
  except Exception as e:
    print("nope "+str(e))

  if(eol==len(target)): # if we've reached the end of every line, we're done
    break

