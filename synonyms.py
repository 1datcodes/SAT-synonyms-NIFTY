'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Oct. 24, 2014.
'''

import math
import re


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    '''

    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    '''

    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]

    return dot_product / (norm(vec1) * norm(vec2))


def get_sentence_lists(text):
	'''This function takes in a string text, and returns a list which contains lists of strings, one list for each
sentence (as defined below) in the string text. A list representing a sentence is a list of the individual
words in the sentence, each one in all-lowercase.'''

	sen_delimiter = r'[.!?]'
	word_delimiter = r"[\s',.:;!?-]"

	output = []
	sentences = re.split(sen_delimiter, text.lower())
	output = [re.split(word_delimiter, sentence) for sentence in sentences if sentence]
	output = [[word for word in sentence if word] for sentence in output if sentence]
	output = [sentences for sentences in output if sentences]

	return output

def get_sentence_lists_from_files(filenames):
	'''This function takes in a list of strings filenames, each one the name of a text file, and returns the list of
every sentence contained in all the text files in filenames, in order. The list is in the same format as in
Part a, but with the files rather than a string serving as the source of the text..'''

	output = []
	for filename in filenames:
		with open(filename, 'r') as file:
			text = file.read()
			output.append(get_sentence_lists(text))
	return output


def build_semantic_descriptors(sentences):
	'''This function takes in a list sentences which contains lists of strings representing sentences, and returns
a dictionary d such that for every word w that appears in at least one of the sentences, d[w] is itself a
dictionary which represents the semantic descriptor of w (note: the variable names here are arbitrary).'''

	output = {}
	for sentence in sentences:
		for words in sentence:
			for word in words:
				if word not in output:
					output[word] = {}
					for other_word in words:
						if other_word != word:
							if other_word in output[word]:
								output[word][other_word] += 1
							else:
								output[word][other_word] = 1
				else:
					for other_word in words:
						if other_word != word:
							if other_word in output[word]:
								output[word][other_word] += 1
							else:
								output[word][other_word] = 1
	return output

def most_similar_word(word, choices, semantic_descriptors):
	'''This function takes in a string word, a list of strings choices, and a dictionary semantic_descriptors
which is built according to the requirements for build_semantic_descriptors, and returns the element
of choices which has the largest semantic similarity to word, with the semantic similarity computed using
the data in semantic_descriptors.'''

	max_similarity = 0
	most_similar = ""
	for choice in choices:
		if word not in semantic_descriptors or choice not in semantic_descriptors:
			similarity = -1
			continue
		else:
			similarity = cosine_similarity(semantic_descriptors[word], semantic_descriptors[choice])

		if similarity > max_similarity:
			max_similarity = similarity
			most_similar = choice
		elif similarity == max_similarity:
			if list(choices).index(choice) < list(choices).index(most_similar):
				most_similar = choice
	return most_similar


def run_similarity_test(filename, semantic_descriptors):
	'''This function takes in a string filename which is a file in the same format as test.txt, and returns the
percentage of questions on which most_similar_word() guesses the answer correctly using the semantic
descriptors stored in semantic_descriptors.'''
	num_problems = 0
	num_correct = 0
	with open(filename, 'r') as file:
		lines = file.readlines()
		num_problems = len(lines)
		for line in lines:
			response = most_similar_word(line.split()[0], line.split()[2:], semantic_descriptors)
			if response == line.split()[1]:
				num_correct += 1
	print("Number of questions:", num_problems, "\nPercent correct:", (num_correct / num_problems * 100))


def main():
	# print(get_sentence_lists("Hello, Jack. How is it going? Not bad; pretty good, actually... Very very good, in fact."))
	# print(get_sentence_lists_from_files(["test2.txt"]))
	# print(build_semantic_descriptors(get_sentence_lists("I am a sick man. I am a spiteful man. I am an unattractive man. I believe my liver is diseased. However, I know nothing at all about my disease, and do not know for certain what ails me.")))
	# print(most_similar_word("good", ["bad", "nice", "great"], build_semantic_descriptors(get_sentence_lists("good is for bad. good is great. good is definitely great."))))
	run_similarity_test("test.txt", build_semantic_descriptors(get_sentence_lists_from_files(["swans-way.txt", "war-and-peace.txt"])))

main()
