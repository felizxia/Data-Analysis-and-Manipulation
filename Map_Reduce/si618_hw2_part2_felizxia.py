from mrjob.job import MRJob
from mrjob.step import MRStep
import re
f_word=re.compile(r"[a-zA-Z']+")
class MRMostUsedWord(MRJob):
    def mapper_get_words(self, _, line):
        for word in f_word.findall(line):
            yield (word.lower(),1)

    def combiner_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_find_max_word(self, _, word_count_pairs):
        yield (None,(word, sum(counts)))
    def steps(self):
        return [
            MRStep(mapper=mapper_get_words,
                    combiner=combiner_count_words,
                    reducer=reducer_count_words),
                    MRStep(reducer=reducer_find_max_word)
                ]