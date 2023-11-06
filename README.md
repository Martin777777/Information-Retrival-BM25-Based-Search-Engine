# README

Name: **Ma Zixiao**

UCD Number: **19206230**

Applicable Corpus: **Both small and large corpus**

## 1. Program Guidance

### 1.1 Submission

- large_search.py: The file that contains the program running for the large corpus
- small_search.py: The file that contains the program running for the small corpus
- README.md: The file that describes what the programs can do and how to run them

### 1.2 small_search.py

To run the program in small_search.py correctly, we have to be in the correct dictionary: the program will be run in the same dictionary as the README.md file in COMP3009J-corpus-small (the README.md file mentioned is not this file but the file in the dictionary COMP3009J-corpus-small).

#### 1.2.1 BM25

This part is the implementation of the BM25 of Information Retrieval which does some processing on the documents for the small corpus and allows users searching for the documents they want by using queries (details are in the comments of the code). Users can type the following commend for this part of functionality:

```
python small_search.py -m manual
```

At the beginning of this program, the program will check if the file named index.json exists. If the file does not exist, the program will traverse the documents to generate the index and create index.json to store the index. If the file exists, the program will load the data in index.json for querying.

After the program creating the index or loading the index from the file index.json, users can then input their queries and get the id of the top 15 documents will be output with their rank and their similarity scores. Here's an example:

```
Enter query: experimental techniques in shell vibration

Results for query [experimental techniques in shell vibration]
1 847 14.790586036998121
2 764 14.076815153479739
3 1036 13.016786951638128
4 844 12.42380661620841
5 848 12.030244861217835
6 953 11.946600863140395
7 846 11.643234803567463
8 42 11.255492384299583
9 1042 11.041411145493704
10 739 10.91086569329589
11 1038 10.69809682823075
12 1043 10.33364451449825
13 1037 10.076319919949192
14 1126 9.833872160103088
15 552 9.62482342910077
```

#### 1.2.2 Evaluation

This part uses the standard queries that are part of the corpus provided to evaluate the effectiveness of the BM25 approach. Users can type the following commend for this part of functionality:

```
python small_search.py -m evaluation
```

At the beginning of this program, the standard queries are read from the "queries.txt" for further retrieval and evaluation. A output file is created which contains the output for each query. The approach for the number of result for each query is explained in the comment of the code.

In the output file, there are six fields on each line, which are the query id, the string Q0, the document id, the rank of the documents in the result for this query, the similarity score for the document and this query, the name of the run (the UCD student ID number of the author). Here's an example:

```
1 Q0 51 1 27.879077192807266 19206230
1 Q0 486 2 26.81170800141192 19206230
1 Q0 12 3 23.85488215397008 19206230
1 Q0 184 4 22.98478405611766 19206230
1 Q0 878 5 21.510897443619182 19206230
1 Q0 665 6 18.86716581692177 19206230
1 Q0 573 7 18.659609145958246 19206230
1 Q0 944 8 17.097112191120996 19206230
2 Q0 12 1 34.97988660065086 19206230
3 Q0 485 1 27.39371449078019 19206230
3 Q0 5 2 25.924098205645926 19206230
3 Q0 144 3 24.793694397945472 19206230
3 Q0 399 4 23.576162142890837 19206230
3 Q0 91 5 20.920412233887824 19206230
3 Q0 90 6 19.996960116244637 19206230
3 Q0 181 7 18.28767996827584 19206230
3 Q0 579 8 17.00121108522087 19206230
4 Q0 488 1 39.86878552301133 19206230
4 Q0 166 2 39.670921370231426 19206230
4 Q0 1061 3 33.76134985675809 19206230
4 Q0 1189 4 31.94571027318794 19206230
4 Q0 1315 5 31.30762539576684 19206230
5 Q0 103 1 20.61555206784412 19206230
5 Q0 1032 2 17.92310940392978 19206230
5 Q0 401 3 17.825051531634756 19206230
5 Q0 943 4 16.672162292162866 19206230
5 Q0 552 5 16.43747384523085 19206230
5 Q0 1296 6 15.48307075434424 19206230
5 Q0 968 7 14.741390885713294 19206230
5 Q0 625 8 14.661034088107971 19206230
5 Q0 1374 9 12.742268698279824 19206230
5 Q0 746 10 12.075135966994035 19206230
5 Q0 488 11 12.03120781356852 19206230
5 Q0 163 12 11.93298407402396 19206230
5 Q0 849 13 11.854310439781312 19206230
5 Q0 368 14 11.633967226289604 19206230
5 Q0 172 15 11.097337624134541 19206230
5 Q0 1391 16 11.09624539565426 19206230
5 Q0 575 17 11.028479461289708 19206230
5 Q0 1272 18 11.009595951196005 19206230
5 Q0 824 19 10.980577302838931 19206230
5 Q0 981 20 10.960733129318164 19206230
5 Q0 1379 21 10.909666984335017 19206230
5 Q0 650 22 10.809049609759379 19206230
5 Q0 328 23 10.533109906609024 19206230
5 Q0 1295 24 10.490709211258542 19206230
5 Q0 342 25 10.487775347684437 19206230
5 Q0 410 26 10.466743391443499 19206230
5 Q0 574 27 10.457420736517015 19206230
5 Q0 332 28 10.316228349108563 19206230
5 Q0 451 29 10.21840510722919 19206230
5 Q0 185 30 10.217383772129725 19206230
5 Q0 77 31 9.831315522810552 19206230
...
```

After creating this file, this program calculates and prints these evaluation metrics: Precision, Recall, P@10, R-precision, MAP, bpref and NDCG@10. For each metric, this program outputs the average score for all the queries provided. Here's an example:

```
Evaluation results:
Precision:   0.11227623969484422
Recall:      0.6469078251118998
P@10:        0.3017777777777778
R-precision: 0.3941476237509334
MAP:         0.4002028420193987
bpref:       0.37001480857276403
NDCG:        0.3600584432262317
```

### 1.3 large_search.py

To run the program in large_search.py correctly, we have to be in the correct dictionary: the program will be run in the same dictionary as the README.md file in COMP3009J-corpus-large (the README.md file mentioned is not this file but the file in the dictionary COMP3009J-corpus-large).

#### 1.2.1 BM25

This part is the implementation of the BM25 of Information Retrieval which does some processing on the documents for the large corpus and allows users searching for the documents they want by using queries (details are in the comments of the code). Users can type the following commend for this part of functionality:

```
python large_search.py -m manual
```

At the beginning of this program, the program will check if the file named index.json exists. If the file does not exist, the program will traverse the documents to generate the index and create index.json to store the index. If the file exists, the program will load the data in index.json for querying.

After the program creating the index or loading the index from the file index.json, users can then input their queries and get the id of the top 15 documents will be output with their rank and their similarity scores. Here's an example:

```
Enter query: magnet schools considered successful districts created

Results for query [magnet schools considered successful districts created]
1 GX265-80-0451668 16.175045969510396                                     
2 GX257-23-14105637 16.15313148382828                                     
3 GX031-39-7722208 16.09184203390751                                      
4 GX255-52-0450453 15.977345760558503                                     
5 GX255-75-6596681 15.9740897158151                                       
6 GX252-15-14240989 15.949351611661545
7 GX233-74-3391812 15.928977069219888
8 GX250-34-15846061 15.865339916115389
9 GX253-03-11964071 15.810519108143438
10 GX263-96-12791397 15.717985966535998
11 GX045-56-15633018 15.539178524038562
12 GX025-60-5876656 15.5289927560608
13 GX233-90-14371690 15.520328620532515
14 GX266-32-0309939 15.485201876471855
15 GX234-92-7198701 15.478424809453564
```

#### 1.2.2 Evaluation

This part uses the standard queries that are part of the corpus provided to evaluate the effectiveness of the BM25 approach. Users can type the following commend for this part of functionality:

```
python large_search.py -m evaluation
```

At the beginning of this program, the standard queries are read from the "queries.txt" for further retrieval and evaluation. A output file is created which contains the output for each query. The approach for the number of result for each query is explained in the comment of the code.

In the output file, there are six fields on each line, which are the query id, the string Q0, the document id, the rank of the documents in the result for this query, the similarity score for the document and this query, the name of the run (the UCD student ID number of the author). Here's an example:

```
701 Q0 GX232-43-0102505 1 9.034011396923825 19206230
701 Q0 GX255-56-12408598 2 8.663648348014338 19206230
701 Q0 GX229-87-1373283 3 8.609869565555432 19206230
701 Q0 GX253-41-3663663 4 8.531288841737158 19206230
701 Q0 GX064-43-9736582 5 8.49862969536831 19206230
701 Q0 GX268-35-11839875 6 8.472766293356193 19206230
701 Q0 GX231-53-10990040 7 8.40033919727388 19206230
701 Q0 GX262-28-10252024 8 8.341923805181803 19206230
701 Q0 GX063-18-3591274 9 8.334242551587755 19206230
701 Q0 GX263-63-13628209 10 8.213608354064021 19206230
701 Q0 GX253-57-7230055 11 8.207045672108341 19206230
701 Q0 GX262-86-10646381 12 8.133131367061406 19206230
701 Q0 GX000-48-10208090 13 8.130574672389251 19206230
701 Q0 GX128-96-12152039 14 8.126422272588519 19206230
701 Q0 GX255-59-12399984 15 8.11804467540209 19206230
701 Q0 GX006-76-15945590 16 8.069942684810348 19206230
701 Q0 GX068-83-6288039 17 8.06086367192437 19206230
701 Q0 GX025-72-6112588 18 8.03927901787393 19206230
701 Q0 GX253-43-11798479 19 7.966255355327415 19206230
701 Q0 GX228-89-9137293 20 7.960688908261643 19206230
701 Q0 GX034-61-5088345 21 7.956671231114019 19206230
701 Q0 GX098-89-15335232 22 7.952698283400723 19206230
701 Q0 GX261-99-14766455 23 7.947639737988489 19206230
701 Q0 GX268-22-14058611 24 7.936040744455776 19206230
701 Q0 GX015-20-10573408 25 7.918913999525085 19206230
701 Q0 GX270-89-3515323 26 7.821743379861869 19206230
701 Q0 GX233-16-2747850 27 7.804649101085175 19206230
701 Q0 GX056-35-8200518 28 7.7909959691897015 19206230
701 Q0 GX233-37-7282946 29 7.768920088778846 19206230
701 Q0 GX271-83-9629845 30 7.762998391097799 19206230
701 Q0 GX252-94-7854611 31 7.754936938908733 19206230
701 Q0 GX267-36-5641094 32 7.740818060266042 19206230
701 Q0 GX251-17-4053346 33 7.721990945213063 19206230
701 Q0 GX241-10-8918222 34 7.713524820874871 19206230
702 Q0 GX081-52-6506700 1 66.06174444317278 19206230
702 Q0 GX049-73-2310771 2 65.27758126258487 19206230
702 Q0 GX005-38-5649730 3 65.00065937359875 19206230
702 Q0 GX001-44-13913188 4 64.70741975439154 19206230
702 Q0 GX008-12-0372379 5 62.3557442464315 19206230
702 Q0 GX048-61-5729137 6 61.87452306892458 19206230
702 Q0 GX008-55-11611507 7 60.53403375215644 19206230
702 Q0 GX267-08-1070198 8 60.44425085526536 19206230
702 Q0 GX267-05-8546339 9 60.43956175662844 19206230
702 Q0 GX253-71-4019096 10 59.94595140900101 19206230
702 Q0 GX027-18-3385268 11 58.36612390355843 19206230
702 Q0 GX247-40-9250915 12 57.90936074936389 19206230
702 Q0 GX271-87-9154916 13 57.07680660212691 19206230
702 Q0 GX237-12-11943678 14 57.03399602628058 19206230
702 Q0 GX026-93-5761284 15 56.70286804592169 19206230
702 Q0 GX059-28-7601493 16 55.60313584047484 19206230
...
```

After creating this file, this program calculates and prints these evaluation metrics: Precision, Recall, P@10, R-precision, MAP, bpref and NDCG@10. For each metric, this program outputs the average score for all the queries provided. Here's an example:

```
Evaluation results:
Precision:   0.4110694521851232  
Recall:      0.9078031628553356  
P@10:        0.5592592592592591  
R-precision: 0.5138978484151085  
MAP:         0.5507348144937256  
bpref:       0.5459722043201932  
NDCG:        0.5215694967259593  
```

## 2. Performance

### 2.1 Device for Testing

The performance is tested by the author's laptop. The configuration of the laptop (Lenovo Legion Y7000P) is shown below:

- Processer: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz   2.59 GHz
- RAM: 16.0 GB

### 2.2 Small Corpus

- Time for generating index and store it in a file: **0.68s**
- Time for loading index file: **0.05s**
- Time for retrieving all the queries in queries.txt and evaluate them: **0.1s**

### 2.3 Large Corpus

- Time for generating index and store it in a file: **42s**
- Time for loading index file: **3.4s**
- Time for retrieving all the queries in queries.txt and evaluate them: **0.18s**