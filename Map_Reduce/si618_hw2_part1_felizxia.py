from mrjob.job import MRJob
import re
f_word=re.compile(r"[a-zA-Z']+")
class MRMostUsedWord(MRJob):
    def mapper(self,_,line):
        for word in f_word.findall(line):
            yield (word.lower(),1)
    def reducer(self,word, counts):
        yield (word, sum(counts))

if __name__ == '__main__':
    MRMostUsedWord.run()
