import math


class BM25(object):

    K1 = 1.5
    B = 0.75
    EPSILON = 0.25

    def __init__(self, corpus):
        self.corpus = corpus
        self.len_corpus = len(corpus)
        self.dl = [float(len(d)) for d in corpus]
        self.avgdl = sum(self.dl) / self.len_corpus
        self.f = []
        self.df = {}
        self.idf = {}
        self.avg_idf = 0

        for i, doc in enumerate(self.corpus):
            print(i)
            frequencies = {}

            for word in doc:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.f.append(frequencies)

            for word, frequency in dict.items(frequencies):
                if word not in self.df:
                    self.df[word] = 0
                self.df[word] += 1

        for word, frequency in dict.items(self.df):
            self.idf[word] = math.log(self.len_corpus - frequency + 0.5) - math.log(frequency + 0.5)

        self.avg_idf = sum(map(lambda k: float(self.idf[k]), self.idf.keys())) / len(self.idf.keys())

        print(self.avg_idf)
        print(self.idf)

    def get_score(self, document, index):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            idf = self.idf[word] if self.idf[word] >= 0 else self.EPSILON * self.avg_idf
            score += (idf * self.f[index][word] * (self.K1 + 1)
                      / (self.f[index][word] + self.K1 * (
                                1 - self.B + self.B * self.dl[index] / self.avgdl)))
        print(score)
        return score

    def get_scores(self, document):
        scores = []
        for index in range(self.len_corpus):
            score = self.get_score(document, index)
            scores.append(score)
        return scores

    def ranked(self, query, length):
        """Returns the `length` most relevant documents according to `query`"""
        scores = [(index, score) for index, score in enumerate(self.get_scores(query))]
        scores.sort(key=lambda x: x[1], reverse=True)
        indexes = scores
        return indexes[:length]

