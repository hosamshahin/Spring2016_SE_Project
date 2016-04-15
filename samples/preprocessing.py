from __future__ import print_function
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os, re, string, ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return head, tail

# split camel case tokens
_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_spaces(s):
    """
    convert camel case into spaces seperated
    """
    subbed = _underscorer1.sub(r'\1 \2', s)
    return _underscorer2.sub(r'\1 \2', subbed).lower()


def preprocessing(input_file, output_file):
    # replace the punctuations with space
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    # stemming
    stemmer = PorterStemmer()

    with open(input_file,'r') as inFile, open(output_file,'w') as outFile:
        for line in inFile:
            # replace punctuations and convert camel case into space seperated
            line_witout_puncs = ' '.join([camel_to_spaces(word) for word in line.translate(replace_punctuation).split()
                  if len(word) >=4 and word not in stopwords.words('english')])

            # stemming
            singles = []
            for plural in line_witout_puncs.split():
                singles.append(stemmer.stem(plural))
            line_stemmed = ' '.join(singles)

            # Remove language keywords

            print(line_stemmed, file=outFile)

project_path = '/home/hshahin/workspaces/spring2016_se_project/data/androidannotations'

project_files = [os.path.join(root, name)
             for root, dirs, files in os.walk(project_path)
             for name in files
             if name.endswith((".java"))]

for source_file in project_files:
    head, tail = path_leaf(source_file)
    proc_file = os.path.join(head , tail + '.proc')
    preprocessing(source_file, proc_file)
