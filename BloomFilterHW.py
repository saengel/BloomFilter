# Sarah Engel
# May 2nd, 2018
# Professor Broder
# Data Structures

import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        p = maxFalsePositive
        n = numKeys
        d = numHashes
        
        # Using equation B to find fe
        phee = (1 -((p)**(1/d)))
        
        # Plugging in fe to equation D to find N (aka size of bits needed)
        N = (d)/(1-((phee)**(1/n)))
        
        return int(N) # Casted to int because you can't have a decimal size
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    # will need to use __bitsNeeded to figure out how big
    # of a BitVector will be needed       
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        self.__n = numKeys   
        self.__d = numHashes  
        self.__p = maxFalsePositive
        self.__N = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitVector = BitVector(size = self.__N)    
        
    # accessors
    def getLen(self):       return self.__bitVector.length()
    def getNumHash(self):   return self.__d

    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        # set to default h for the first time through
        prevBucket = 0  
        
        # hash appropriate number of times (numHashes) and set the bits
        # counting how many get set to 1       
        for i in range (0, self.__d):
            bucket = BitHash.BitHash(key, prevBucket) % self.__N
            
            if self.__bitVector[bucket] != 1:
                self.__bitVector[bucket] = 1
            
            # next time we bit hash, we've updated our h
            # with the previous bucket
            prevBucket = bucket
 
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        
        # set to default h for the first time because of bitHash function
        # specifications
        prevBucket = 0  
        
        for i in range(0, self.__d):
            
        # hashes that number of times, and returns T/F appropriately
        # if 1, then result = T
            bucket = BitHash.BitHash(key, prevBucket) % self.__N
        
            # check first
            if self.__bitVector[bucket] != 1:
                return False
            
            # next time we BitHash, we've updated our h
            # with the previous bucket
            prevBucket = bucket
              
        # otherwise, if all hash indices were 1s, we return true 
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    def falsePositiveRate(self):
        # Using equation B
        fe = (1 - (self.__d/self.__N))**self.__n
        
        # Using equation A
        proportion = (1 - fe) ** self.__d
        
        return proportion 
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    bf = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fin = open("wordlist.txt")
    line = fin.readline()
    
    # Reading the first 100,000 keys
    for i in range(0, numKeys):
        line = fin.readline()
        bf.insert(line)
    fin.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("The projected false positive rate based on the bits inserted: " \
          + str(bf.falsePositiveRate()))

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    fin = open("wordlist.txt")
    line = fin.readline()
    numMistakes = 0
    
    # Reading the first 100,000 keys
    for i in range(0, numKeys):
        line = fin.readline()
        if bf.find(line) == False:
            numMistakes += 1
    
    print(str(numMistakes) + \
          " number of words were missing from the bloom filter")
  
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    # Number of false positives, ones where we did not insert
    mistakenFind = 0 
    
    # Total number of lines checked
    lines = 0
    
    # Loop through counting number of false positives
    while line:
        lines += 1
        line = fin.readline()
        if bf.find(line) == True:
            mistakenFind += 1 
        
    fin.close() 
    print("There were " + str(mistakenFind) + " accidentally found")
    
    # Print out the percentage rate of false positives.
    # divide actual number of false positives by number of lines
    # to find the proportion 
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    actualProportion = mistakenFind/lines
    print("The actual false positive rate: " + str((actualProportion)))
    
if __name__ == '__main__':
    __main()       

