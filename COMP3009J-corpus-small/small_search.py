import json
import math
import os
import re
import sys
from optparse import OptionParser

from files import porter


# This function is used for the creating the index and store the index and some cache in files.
# The index this function aims to create is a dictionary whose key is the terms and value is a dictionary whose key is
# the id of the documents that involves the term and the value is the bm25 score of the term for the document.
# At the beginning of this function, an empty dictionary is created as the index.
# An empty dictionary named temporary_data is created to store some temporary data which will be later used to
# calculate the data in index and another empty dictionary named document_length is created to store the document length
# Then, every document in the documents dictionary is read and each word in it is tried to be transformed to a term for
# some further processing (the details will be explained in the comments above the code used for the further processing)
# After the process of reading documents, all the terms in the document are stored in temporary_data as keys and
# the value is the dictionary where the keys are the id of the documents that contains the term and the value is
# the term frequency of the term in the document. Moreover, the length of each documents is stored in document_length
# after the document is read and average length of the documents is calculated.
# After the process above is finished, the temporary_data is traversed to calculate the data in index.
# Finally, index is stored in index.json which is to be loaded for querying.
# The details of this function are shown below.
def indexing():

    # set the value of k and b which will be used to calculate the similarity score later
    k = 1
    b = 0.75

    # get the stemming_cache, stopwords and index outside to store data in them so that when the process of creating
    # index is finished, the program has gotten stemming_cache, stopwords and index
    # and do not have to load them from files.

    # stemming_cache is the dictionary where keys are the original words and values are the words after stemming process
    # stemming_cache is used and stored to accelerate the process of stemming.
    global stemming_cache
    # stopwords is the set that stores all the stopwords
    global stopwords
    # index is the dictionary where keys are the terms and values are dictionaries there keys are
    # the id of the documents that involve the term and the values are the bm25 scores of the term for the document.
    # index is in this data structure because in the process of querying, the program can simply add up the scores of
    # the documents that contain each term in the query and no more calculation is needed. Details about this process
    # will be shown in the function of querying.
    global index

    stemmer = porter.PorterStemmer()

    temporary_data = {}

    # read stopwords in the file
    with open("files/stopwords.txt", "r") as stopwords_file:
        for line in stopwords_file:
            stopwords.add(line.strip())

    filenames = os.listdir("documents")

    files_number = 0
    total_length = 0
    document_lengths = {}

    for filename in filenames:
        with open("documents/" + filename, "r") as document:

            # Here is the process of getting the words from the content of the document.
            # This program considers words connected by some punctuations as separate words and 's at the end of
            # words are removed.
            # Numbers including floating point numbers are considered as words, so the dot
            # between two numbers will not be removed.
            # If letters and numbers are together, they will be separated. For example, "123apples" will be
            # separated to "123" and "apples".

            # This line is to remove 's in the document for further extracting
            result = re.sub(r"'s", " ", document.read(), 0)

            # This line is to get the extract tokens from the result processed by the last line
            # What it does is find the letters and numbers including floating point numbers and separate them
            tokens = re.compile("[a-zA-Z]+|\d+\.\d+|\d+", re.A).findall(result)

            # Initialize the length of every document for the count of the number of terms later
            document_length = 0

            # Traverse all the tokens in every document
            for token in tokens:
                # Capitalization of tokens are not considered, so all the tokens will be turned to lower case
                token = token.lower()
                # Make sure that the token is not an empty character and not a stopword
                if token != "" and token not in stopwords:
                    # Here the program tries to find the stemmed form of the token from the cache
                    # The reason why there is a cache for the stemming process is that the process of stemming
                    # is really time-wasting and there are lots of repeated tokens to be stemmed in the process
                    # of indexing, so a cache for stemming saves lots of time.
                    stemmed_word = stemming_cache.get(token, False)
                    if not stemmed_word:
                        stemmed_word = stemmer.stem(token)
                        stemming_cache[token] = stemmed_word
                    # For each term transformed by a word, we check if it is already a key of the temporary_data.
                    value = temporary_data.get(stemmed_word, False)
                    # If the term is already a key of the temporary_data, we just add its frequency in the current
                    # document by one
                    if value:
                        value[filename] = value.get(filename, 0) + 1
                    # If it is not, we store the term in the temporary_data as a key and its corresponding value is
                    # the dictionary that shows that current frequency in the current document is 1.
                    else:
                        temporary_data[stemmed_word] = {filename: 1}
                    # Finally, the document_length is added by 1.
                    document_length += 1

            # Record the length of the document for further calculation of the bm25 score.
            document_lengths[filename] = document_length
            # Add the length of the document to the total length for the calculation of the average length.
            total_length += document_length
        # Add the number of files by 1 for the calculation of the average length.
        files_number += 1

    # Calculate the average length of all the documents
    avg_document_length = total_length / files_number

    # Traverse the temporary_data to get the index.
    # Each item in temporary_data records the terms and all the documents that contains the term and
    # the frequency the term appears in each document that contains it.
    for term, values in temporary_data.items():
        # Get the number of documents that contain the current term.
        appeared_document_number = len(values)
        # The dictionary similarities records the bm25 scores of each document that contains the current term for
        # the current term.
        similarities = {}
        # Calculate the score for each document and add them to the dictionary similarities
        for document_id, value in values.items():
            frequency = value
            document_length = document_lengths[document_id]
            similarity = (frequency * (1 + k)) / (
                    frequency + (k * ((1 - b) + ((b * document_length) / avg_document_length)))) * math.log2(
                (files_number - appeared_document_number + 0.5) / (appeared_document_number + 0.5))
            similarities[document_id] = similarity
        # Store the similarities in the index for the current term.
        index[term] = similarities

    # Store the cache in files
    json.dump(stemming_cache, open("stemming_cache.json", 'w'))
    json.dump(index, open("index.json", 'w'))

    with open("stopwords.txt", "w") as f:
        f.write(str(stopwords))


# This function aims to read cache previously stored by indexing.
# stemming_cache, stopwords and index initialized outside will be gotten
# and the data stored in files will be loaded into them.
def read_cache():

    # Get stemming_cache, stopwords and index initialized outside
    global stemming_cache
    global stopwords
    global index

    # Load the data stored in the files into stemming_cache, index and stopwords
    index = json.load(open("index.json"))
    if os.path.exists("index.json"):
        stemming_cache = json.load(open("stemming_cache.json"))
    if os.path.exists("stopwords.txt"):
        with open("stopwords.txt", "r") as f:
            stopwords = eval(f.read())
    else:
        with open("files/stopwords.txt", "r") as stopwords_file:
            for line in stopwords_file:
                stopwords.add(line.strip())


# This function aims to get the relevant documents of a query ranked by their similarity scores.
def retrieval(query):
    global stemming_cache
    global stopwords
    global index

    # document_scores is a dictionary where keys are the id of documents which are considered relevant to the query
    # and values are the similarities of documents.
    document_scores = {}

    # Extract the tokens in the query.
    result = re.sub(r"'s", " ", query, 0)
    tokens = re.compile("[a-zA-Z]+|\d+\.\d+|\d+", re.A).findall(result)
    stemmer = porter.PorterStemmer()

    # Traverse each token in the query
    # The preprocessing is in the same way as the preprocessing in indexing
    for token in tokens:
        # Transform each word to a term in the same way as the preprocessing
        token = token.lower()
        if token != "" and token not in stopwords:
            stemmed_word = stemming_cache.get(token, False)
            if not stemmed_word:
                stemmed_word = stemmer.stem(token)
                stemming_cache[token] = stemmed_word
            # Check if the current term is stored in index.
            scores = index.get(stemmed_word, False)
            # If the current term is stored in index, get all the documents' id and their corresponding scores
            # and add them to document_scores
            if scores:
                for document_id, score in scores.items():
                    document_scores[document_id] = document_scores.get(document_id, 0) + score
    # Rank the document_score by the similarity scores to get the final output
    output = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    return output


# This function is to receive and process the query input by the user.
# Top 15 relevant document will be printed.
def start_input():
    user_input = input("Enter query: ")

    while user_input != "QUIT":
        output = retrieval(user_input)[:15]
        rank = 1

        print("\nResults for query [{0}]".format(user_input))

        for document_id, score in output:
            print(rank, document_id, score)
            rank += 1
        user_input = input("Enter query: ")


# This function aims to read the file qrels.txt and get the documents with their similarity scores for queries
# and get the documents which are relevant for queries with their similarity scores.
def load_qrels():
    # all_documents_dict is to store the documents with their similarity scores for queries.
    all_documents_dict = {}
    # relevant_documents_dict is to store the documents which are relevant for queries with their similarity scores.
    relevant_documents_dict = {}
    # Here the file qrels.txt is read
    with open("files/qrels.txt", "r") as f:
        # Each line in the file is read and the information is extracted into the two dictionaries.
        for line in f:
            relevance = line.split()
            query_id = relevance[0]
            doc_id = relevance[2]
            score = relevance[3]
            query_result = all_documents_dict.get(query_id, False)
            if query_result:
                query_result[doc_id] = score
            else:
                all_documents_dict[query_id] = {doc_id: score}
            if score != "0":
                relevant_query_result = relevant_documents_dict.get(query_id, False)
                if relevant_query_result:
                    relevant_query_result[doc_id] = int(score)
                else:
                    relevant_documents_dict[query_id] = {doc_id: int(score)}
    return all_documents_dict, relevant_documents_dict


# This function aims to calculate the precision score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def precision(query_id, output):
    # The IDs of documents which are relevant to the query with query_id as its ID is gotten.
    # relevant is the set that stores the information.
    global relevant_documents_set
    relevant = relevant_documents_set[query_id].keys()
    # Traverse the result to get the number of the results and the number of relevant documents in it.
    num_results = 0
    num_relevant = 0
    for item in output:
        num_results += 1
        if item[0] in relevant:
            num_relevant += 1
    return num_relevant / num_results


# This function aims to calculate the recall score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def recall(query_id, output):
    # The IDs of documents which are relevant to the query with query_id as its ID is gotten.
    # relevant is the set that stores the information.
    global relevant_documents_set
    relevant = relevant_documents_set[query_id].keys()
    # Traverse the result to get the number of relevant documents in the result.
    num_relevant = 0
    for item in output:
        if item[0] in relevant:
            num_relevant += 1
    return num_relevant / len(relevant)


# This function aims to calculate the precision@10 score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def precision_at_10(query_id, output):
    # The IDs of documents which are relevant to the query with query_id as its ID is gotten.
    # relevant is the set that stores the information.
    global relevant_documents_set
    relevant = relevant_documents_set[query_id].keys()
    # Traverse the result to get the number of relevant documents in the first 10 documents in the result if the length
    # of the result if bigger than 10. Otherwise, the whole result will be traversed.
    num_relevant = 0
    number = min(len(output), 10)
    for i in range(number):
        if output[i][0] in relevant:
            num_relevant += 1
    # Finally, we divide the number of relevant documents in the result by the smaller value between the length of
    # output and 10
    return num_relevant / number


# This function aims to calculate the R-precision score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def r_precision(query_id, output):
    # The IDs of documents which are relevant to the query with query_id as its ID is gotten.
    # relevant is the set that stores the information.
    global relevant_documents_set
    relevant = relevant_documents_set[query_id].keys()
    # Traverse the result to get the number of relevant documents in the first n documents in the result
    # where n is the length of the relevant documents if the length of the result if bigger than n.
    # Otherwise, the whole result will be traversed.
    num_relevant = 0
    relevant_length = len(relevant)
    number = min(len(output), relevant_length)
    for i in range(number):
        if output[i][0] in relevant:
            num_relevant += 1
    # Finally, we divide the number of relevant documents in the result by the length of the relevant documents
    return num_relevant / relevant_length


# This function aims to calculate the MAP score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def MAP(query_id, output):
    # The IDs of documents which are relevant to the query with query_id as its ID is gotten.
    # relevant is the set that stores the information.
    global relevant_documents_set
    relevant = relevant_documents_set[query_id].keys()
    # pre is the sum of precision at each recall point
    pre = 0
    num_relevant = 0
    rank = 1
    # Traverse the result to get the MAP score
    for item in output:
        if item[0] in relevant:
            num_relevant += 1
            pre += num_relevant / rank
        rank += 1
    return pre / len(relevant)


# This function aims to calculate the bpref score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def bpref(query_id, output):
    # The documents with their similarity scores for queries are gotten here
    global all_documents
    documents = all_documents[query_id]
    # As there is no unjudged document in the small corpus, the documents which do not appear in the file or whose
    # scores are 0 are considered irrelevant documents.
    grades = documents.values()
    num_irrelevant = 0
    contribution = 0
    relevant_length = 0
    # Here the number of relevant documents is calculated.
    for grade in grades:
        if grade != "0":
            relevant_length += 1
    # Traverse the results.
    for item in output:
        doc_id = item[0]
        if documents.get(doc_id, "0") != "0":
            # If the number of irrelevant counted is bigger than the number of relevant documents available,
            # the score won't change anymore, so the loop breaks.
            if num_irrelevant < relevant_length:
                contribution += 1 - num_irrelevant / relevant_length
            else:
                break
        else:
            num_irrelevant += 1
    return contribution / relevant_length


# This function aims to calculate the NDCG@10 score for the query whose id is the parameter query_id.
# The parameter output is the result for the query returned by the retrieval system.
def NDCG_at_10(query_id, output):
    # The documents which are relevant for queries with their similarity scores are gotten here
    global relevant_documents_set
    relevant_documents = relevant_documents_set[query_id]
    # If the number of results is bigger than 10, we pick the DCG score at rank 10.
    # Otherwise, we pick the last DCG score.
    number = min(len(output), 10)
    if number != 0:
        # Here we start at the rank 2 of the result since that at rank 1, the CG score is equal to the grade at rank 1.
        rank = 2
        cumulated_grade = relevant_documents.get(output[0][0], 0)
        for i in range(1, number):
            doc_id = output[i][0]
            grade = relevant_documents.get(doc_id, 0)
            if grade != 0:
                cumulated_grade += grade / math.log2(rank)
            rank += 1

    else:
        return 0

    # In IDCG scores, we pick the same rank as the rank we pick in DCG scores. If the number of results is less
    # than that rank, the actual score we pick is the score at rank n where n is the number of results because
    # in IDCG scores, the score at this rank is the same as the score at the rank we pick in DCG scores in this case.
    ideal_number = min(len(relevant_documents), number)
    ideal_rank = 2
    sorted_grades = sorted(relevant_documents.values(), reverse=True)
    ideal_cumulated_grade = sorted_grades[0]
    for i in range(1, ideal_number):
        ideal_cumulated_grade += sorted_grades[i] / math.log2(ideal_rank)
        ideal_rank += 1

    return cumulated_grade / ideal_cumulated_grade


# This function aims to generate the output content for one query
def generate_output_content(query_id, query_output):
    output_content = ""
    rank = 1
    for doc_id, similarity in query_output:
        output_content += "{0} Q0 {1} {2} {3} 19206230\n".format(query_id, doc_id, rank, similarity)
        rank += 1

    return output_content


# This function aims to get the average precision, recall, precision@10, R-precision, MAP, bpref and NDCG@10 scores
# for the queries in the file queries.txt.
def evaluation():
    output_content = ""

    with open("files/queries.txt", "r") as f:
        precision_score = 0
        recall_score = 0
        precision_at_10_score = 0
        r_precision_score = 0
        MAP_score = 0
        bpref_score = 0
        NDCG_at_10_score = 0
        query_number = 0
        for line in f:
            first_space_index = line.find(" ")
            query_id = line[:first_space_index]
            output = retrieval(line[first_space_index + 1:])

            # The number of output for a query is the integer from of the highest score of the results and
            # the 8th highest score of the results (if the length of the results is less than 8, we take
            # the last score here). This number will also be restricted to the range from 0 to 43. Here the reason why
            # the highest score is taken is that if the score for a query is high, it may mean that there may be
            # many words in the query which are contained by some documents in the corpus, so the number of the output
            # should be relatively high. Furthermore, the 8th highest score is taken to prevent the situation that the
            # document with the highest score get this score because it contains some words in the query which seldom
            # appear in other documents, so the other documents may not be very related to the query.
            # If the differences among scores are big, this approach may not work well since that the highest score and
            # the 8th highest score may not reflect the quality of the whole result returned
            # by the retrieval system well.
            # The experiment shows that the score of precision decreases only a little compared with the fixed number of
            # results (the number is 15) but score for recall increases significantly. Other metrics also increases.
            # Therefore, it is considered that this approach is appropriate.
            if output[7]:
                output_length = min(max(int(output[0][1] + output[7][1]) * 2, 0), 43)
            else:
                output_length = min(max(int(output[0][1] + output[-1][1]) * 2, 0), 43)
            output = output[:output_length]

            output_content += generate_output_content(query_id, output)

            precision_score += precision(query_id, output)
            recall_score += recall(query_id, output)
            precision_at_10_score += precision_at_10(query_id, output)
            r_precision_score += r_precision(query_id, output)
            MAP_score += MAP(query_id, output)
            bpref_score += bpref(query_id, output)
            NDCG_at_10_score += NDCG_at_10(query_id, output)
            query_number += 1
        print("Evaluation results:")
        print("Precision:   {0}".format(precision_score / query_number))
        print("Recall:      {0}".format(recall_score / query_number))
        print("P@10:        {0}".format(precision_at_10_score / query_number))
        print("R-precision: {0}".format(r_precision_score / query_number))
        print("MAP:         {0}".format(MAP_score / query_number))
        print("bpref:       {0}".format(bpref_score / query_number))
        print("NDCG:        {0}".format(NDCG_at_10_score / query_number))

    with open("output.txt", "w") as f:
        f.write(output_content)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-m', action="store", type="string")
    option = parser.parse_args(sys.argv[1:])[0].m

    stemming_cache = {}
    stopwords = set()
    index = {}

    if os.path.exists("index.json"):
        print("Loading BM25 index from file, please wait.")
        read_cache()
    else:
        print("Generating BM25 index from file, please wait.")
        indexing()

    if option == "manual":
        start_input()
    elif option == "evaluation":
        # all_documents stores the documents with their similarity scores for queries
        # relevant_documents_set stores the documents which are relevant for queries with their similarity scores.
        all_documents, relevant_documents_set = load_qrels()

        evaluation()
    else:
        all_documents, relevant_documents_set = load_qrels()

        evaluation()
