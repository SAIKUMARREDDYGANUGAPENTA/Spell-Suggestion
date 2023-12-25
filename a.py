from tabulate import tabulate
# Initialize an empty dictionary
data = {}

# Initialize a variable to keep track of the current key
current_key = None

# Open the text file for reading (use the correct file path)
with open("./G17modifieddata.txt", encoding="utf-8") as f:
    for line in f:
        # Remove leading/trailing whitespaces
        line = line.strip()

        # Check if the line is not empty
        if line:
            # Check if the line ends with a colon to indicate a key
            if line.endswith(":"):
                # Extract the key (remove the colon)
                current_key = line[:-1]
                # Initialize an empty sub-dictionary for the current key
                data[current_key] = {}
            else:
                # Split the line into key and value based on the ":"
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    # Add the key-value pair to the current sub-dictionary
                    if current_key:
                        data[current_key][key] = value

# Print the resulting dictionary
key_list = list(data.keys())

# Print the list of keys
# print(len(key_list))


# ==================removing duplicates============

key_list = set(key_list)
key_list = list(key_list)


#==================generate Ngrams for a word===================


def generateNGrams(n,word):
    nGrams=[]
    i = 0
    size = len(word)
    while((i+n-1)<size):
        nGrams.append(word[i:i+n])
        i+=1
    
    return nGrams

#================Creating Ngram index=============

def creatNIndex(n,vocabulary):
    nIndex = dict()
    for word in vocabulary:
        Ngrams=generateNGrams(n,word)
        for gram in Ngrams:
            if(nIndex.get(gram)==None):
                nIndex[gram]=[word]  
            else:
                tlist=nIndex[gram]
                tlist.append(word)
                nIndex[gram]=tlist
    return nIndex
#================Bigram=============

n=2

#=============Creating bigram for all words===========
Nindex=creatNIndex(n,key_list)


#=============Checking spell===========
def checkSpelling(word,ary):
    print ("checking word .... " + word)
    for str in ary:
        if (str==word):
            return True
    return False


# ===============Generating suggested posting list from the bigram index========

def generateSuggestedList(word,Nindex,n):
    size=len(word)
    i=0
    slist=[]
    while((i+n-1)<size):
        bg=word[i:i+n]
        poslist=Nindex.get(bg)
        if(poslist!=None):
            poslist=list(set(poslist))
            slist.append(poslist)
        i+=1
    return slist

# కథ
# print(generateSuggestedList('అండకోశము',Nindex,n))


# =============Ranking the possible words and generating the correct word===========
 
#  ============checking for the length=====================


def lengthCof(word1,word2):
    len1=len(word1)
    len2=len(word2)
    if(len1>len2):
        k=((len2/len1))
        return k
    else:
        k=((len1/len2))
        return k

# ===================Rank the words in the slist===================


def ranking(word,slist,m):
    
    ranks=dict()
    
    for list in slist:
        for str in list:
            freq=ranks.get(str)
            if(freq==None):
                ranks[str]=1
            else:
                ranks[str]=freq+1


# ==============sorting according to the items====================
    

    sortRanks=sorted(ranks.items(), key=lambda x:x[1],reverse=True)
    sortRanks=dict(sortRanks[0:m])


# =======adding length to the frequency============
    
    for key in sortRanks.keys():
        freq = sortRanks.get(key)
        lengthscore=lengthCof(word,key)
      
        score = freq + lengthscore
        sortRanks[key]=score

# =================again sorting it =======================
   
    sortRanks=sorted(sortRanks.items(), key=lambda x:x[1],reverse=True)   
   
    sortRanks=dict(sortRanks)
   
    return sortRanks

# slist=generateSuggestedList('అండకోశము',Nindex,n)
# print(len('అండకోశము'))
# print(ranking('అండకోశమ',slist))

# ============Calculate the Rank based on the first char=============


def refine1(word, ranks):
    sortedRanks = {}
    for key in ranks.keys():
        freq = 0
        if word[0] == key[0]:
            freq = 1
        score = freq + ranks.get(key)
        ranks[key] = score
    sortedRanks = dict(sorted(ranks.items(), key=lambda x: x[1], reverse=True))
    return sortedRanks


# ============Calculate the Rank based on the last char=============

def refine2(word, ranks):
    len1 = len(word)
    for key in ranks.keys():
        len2 = len(key)
        freq = 0
        if word[len1 - 1] == key[len2 - 1]:
            freq = 1
        score = freq + ranks.get(key)
        ranks[key] = score
    sortedRanks = dict(sorted(ranks.items(), key=lambda x: x[1], reverse=True))
    return sortedRanks


# =========================Checking the function================================

# list2 = ['అండకోశము','అంటుమెడ','అంతఃకరణము','అంతము','అంతరాత్మ','అంతరాయం','అంతరాయము','ఎదురుపాటు','ఎదురుమోయు', 'ఎదురేగు','ఓష్ట','ఓసరింత','ఓసరిల్లు','ఓసరు','ఓహటము','కముంజూ','కముచు','కముడి','కముడివీడిచె','కమునకు','కలిగొట్టు','కలితనము','కలితము','కలిద్రుమము','కలిపి','కుథము','కుదండంబు','కుదప', 'కుదరము','కుదించు','ఖండీరము','ఖండువా','ఖందడముకానిది','ఖందితము','ఖందీరము','చేలువడి','చేలువమిరియము','చేల్లకము','చేల్లగడ్డ','చేల్లడము','టాటోటు', 'టాటోటుకాండు','టాడా','టాడింపక','దృశ్యం','దృశ్యత','దెచ్చెదమునీకు','దెజవమేను','దెప్పరించు','దెప్పరిల్లు','ఫాలనేత్రుండు',]

# list1 = ['అండకోశమ','అంటుమె','అంతఃకరణమ','అంతమ','అంతరాత్', 'అంతరాయ', 'అంతరాయమ','ఎదురుపటు', 'ఎదురుమోయ', 'ఎదురేగ','ఓష్', 'ఓసరిం', 'ఓసరిల్ల', 'ఓసర', 'ఓహటమ', 'కముంజ', 'కముచ', 'కముడ', 'కముడివడిచె', 'కమునక','కలిగొట్ట', 'కలితనమ', 'కలితమ', 'కలిద్రమము', 'కలిప','కుథమ', 'కుదండంబ', 'కుద', 'కదరము', 'కుదించ','ఖండీరమ', 'ఖండువ', 'ఖందడమకానిది', 'ఖందితమ', 'ఖందీరమ','చేలువడ', 'చేలువమిరియమ', 'చేల్లకమ', 'చేల్గడ్డ', 'చేల్లడమ','టాటోట', 'టాటోటుకాండ', 'టాడ', 'టాడిపక','దృశ్య', 'దృశ్య', 'దెచ్చెదమునీక', 'దెజవమేన', 'దెప్పరించ', 'దెప్పరిలలు','ఫాలనేత్రుడు']


# def findPrecision(list1,list2):
#     size = len(list1)
#     i=0
#     matched = 0
#     while (i<size):
#         slist = generateSuggestedList(list1[i],Nindex,n)
#         crtedword = ranking(list1[i],slist,30); 
#         if(crtedword==list2[i]):
#             matched=matched + 1
#         i=i+1
#     return ("Accuracy is: " + str(matched/size))

# findPrecision(list1,list2)



#=========Function for printing==============

def language(inner_key,Input_word):


# Check if the fixed outer key exists in the dictionary
  if Input_word in data:
      # Access the nested dictionary associated with the fixed outer key
      inner_dict = data[Input_word]

      # Check if the inner key exists in the inner dictionary
      if inner_key in inner_dict:
          # Retrieve and print the value
          value = inner_dict[inner_key]
          print('----------------------------------------------')
          print(f"{value}")
          print('----------------------------------------------')
      else:
          print(f"'{inner_key}' not found in '{Input_word}'")
  else:
      print(f"'{Input_word}' not found in the dictionary.")


def listwordfun(ranks,Input_word):
    print("-----------------------------------------------------------------------------")
    print("suggested words and their score are :")
    print("-----------------------------------------------------------------------------")

    table_data = []
    for idx, (key, value) in enumerate(ranks.items(), start=1):
        table_data.append([f"{idx}:{key}", f"{value:.5f}"])

    headers = ["Word", "Rank"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("-----------------------------------------------------------------------------")
    val=input("If you satisfied with the above list Enter 'Yes/yes' else Enter 'No/no' :")
    print("-----------------------------------------------------------------------------")

    if(val.lower()=='yes'):
        valid = True
        while valid:
            y = int(input("Enter the number according to the word in the above list: ")) - 1
            keys_list = list(ranks.keys())
            if 0 <= y < len(keys_list):
                selected_key1 = keys_list[y]
                valid = False
                ab=int(input("If you want to know the meaning in different languages enter 1 else enter 0 : "))

                if ab==1:
                  printfun(selected_key1)
                else:
                  print("-----------------------------------------------------")
            else:
                print("Invalid input. Please enter a valid number.")
    else:
        with open('your_file.txt', 'a', encoding='utf-8') as file:
            file.write(Input_word + '\n')
        print("--------------------------------------------------------------------------------------")

        print('we will provide best words as soon as possible')
        print("--------------------------------------------------------------------------------------")


def printfun(Input_word):

    print("Use Serial Numbers of languages as input \n")
    print("1. English")
    print("2. Hindi")
    print("3. Tamil")
    print("4. Kannada")
    print("5. Exit")
    
    while True:
        num = int(input("Enter Number: "))
        
        if num == 1:
            language("English",Input_word)
            print("If you want more please enter the other number.")
        elif num == 2:
            language("Hindi",Input_word)
            print("If you want more please enter the other number.")
        elif num == 3:
            language("Tamil",Input_word)
            print("If you want more please enter the other number.")
        elif num == 4:
            language("Kannada",Input_word)
            print("If you want more please enter the other number.")
        elif num == 5:
            print("-----------------------------------------------------")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 5.")
    
#=============Taking input=============
print("\n\n \t \t Enhanced Language Accuracy Spelling Correction In Telugu \n\n")
print("--------------------------------------------------------------------------------------")
Input_word = input("Enter the seacrh word:  ")
print("--------------------------------------------------------------------------------------")


#=============checking status============

status=checkSpelling(Input_word,key_list)


#=================After checking============

# status = True  # Assuming status is True, change it according to your logic

if status:
    print("We found your correct word")
    # print("The bigrams for given word are :",generateNGrams(2,Input_word))
    print("--------------------------------------------------------------------------------------")
    h143 = (input("Do you want to know its meaning in other languages (Yes / No): "))
    print("--------------------------------------------------------------------------------------")
    if h143.lower() == "yes":
        printfun(Input_word)
    elif(h143.lower() == 'no'):
       print("-----------------------------------------------------")

   
else:
    slist=generateSuggestedList(Input_word,Nindex,n)
    print("--------------------------------------------------------------")
    print('Oops! Its wrongly spelt!')
    print('We found you few suggestions !')
    m=int(input("How many suggestions do you need ? (<30) :"))
    print("--------------------------------------------------------------")
    if m>=30:
        m=30
    elif m<=0:
        m=10
    print("-----------------------------------------------------------------------------")
    print("Suggestions and their Scores: ")
    print("-----------------------------------------------------------------------------")
    ranks=ranking(Input_word,slist,m)


# Assuming ranks is a dictionary containing words and their ranks

# Example ranks dictionary
   

    table_data = []
    for idx, (key, value) in enumerate(ranks.items(), start=1):
        table_data.append([f"{idx}:{key}", f"{value:.5f}"])

    headers = ["Word", "Rank"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    

    val=input("Do you get your required word? (Yes / No):  ")
    if(val.lower()=='yes'):
        valid = True
        while valid:
            y = int(input("Enter the serial number of your word:  ")) - 1
            keys_list = list(ranks.keys())
            if 0 <= y < len(keys_list):
                selected_key1 = keys_list[y]
                valid = False
                ab=(input("Do you want to know its translations in other languages? (Yes / No):  "))

                if ab=='1' or ab.lower()=='yes':
                  printfun(selected_key1)
                elif ab == '0' or ab.lower() == 'no':
                  print("-----------------------------------------------------")
            else:
                print("Invalid input. Please enter a valid number.")
   
   
    else:
        print("--------------------------------------------------------------")
        print("Enter '1' : if you are confident with the first letter of your word ?")
        print("Enter '2' : if you are confident with the last letter of your word ? ")
        print("--------------------------------------------------------------")
        num=int(input("Enter Value :  "))
        print("--------------------------------------------------------------")
        if(num==2):
            output2=refine2(Input_word,ranks)
            listwordfun(output2,Input_word)
        else:
            output1=refine1(Input_word,ranks)
            listwordfun(output1,Input_word)
    


# Taking input
user_input = float(input("Upload your review (1 to 5): ")) 
print("--------------------------------------------------") # Accepts float values
print("\nYour rating has been recorded! Thank You!\n\n")

adjusted_input = max(1, min(round(user_input), 5))  

with open('Review.txt', 'a', encoding='utf-8') as file:  
    file.write(f'{adjusted_input}\n')

if adjusted_input <= 3:
    remarks = input("Any remarks? : ")
    print("\nYour remarks are recorded! We will resolve them asap!\n\n")
 
    with open('remarks.txt', 'a', encoding='utf-8') as remarks_file:  
        remarks_file.write(f'{remarks}----{Input_word}\n')




print("----------------Thank You-----------------")