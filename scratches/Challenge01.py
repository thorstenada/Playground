import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import nltk
import spacy
nltk.download('stopwords')
nltk.download('punkt')
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

#Stopwords
tokenized_stopwords = set(stopwords.words('english'))

#Fx for transforming sentences without stopwords and punctuation
def getTerms(sentences):
    tokens = nltk.word_tokenize(sentences)
    words = [w.lower() for w in tokens if w.isalnum()]
    words = [w.lower() for w in words if w not in tokenized_stopwords]
    return words

#Are both sentences related
def relatedSentences(sentence, target):
    bestCount = 0
    answer = ""
    for sent in target:
        currentCount = sum([sent.count(i) for i in set(sentence)])
        if currentCount > bestCount:
            bestCount = currentCount + bestCount
            answer = ' '.join(sent)
    return bestCount

#xls_file = pd.ExcelFile(r'C:\Users\david\Documents\Python Scripts\WHU Hackathon\Challenge01_Siemens\Artificial Intelligence Companies.xlsx')
xls_file = pd.ExcelFile(r'~/Desktop/Artificial Intelligence Companies.xlsx')
xls_file
xls_file.sheet_names
dfAIC = xls_file.parse('Sheet1')    # we name our dataframe dfAIC
dfAIC.head()

# Generate our reference text as a parameter "ref01". Later on we will compare the other companies descriptions to this reference text to find out about their similarity
target_text = 'Our Al powered solutions address major challenges that are facing the healthcare field. Right now, the demand for diagnostic services is outpacing the supply of experts in the workforce. Developing solutions for managing this ever increasing workload is a crucial task for the healthcare sector. Moreover, as the workload is growing, diagnostics and treatment are also becoming more complex. Diagnostic experts and physicians need a new set of tools that can handle large volumes of medical data quickly and accurately, allowing you to make more objective treatment decisions based on quantitative data and tailored to the needs of the individual patient. To provide this new toolset, we will need to draw on the power of artificial intelligence (AI).'
target_token = getTerms(target_text.lower())
#target_token_alpha =[x.lower() for x in target_token if target_token.isalpha()]
#target_token_clean = [x for x in target_token if x not in tokenized_stopwords]
print(target_token)

#Create list of tokenized descriptions, calculate matching counts and add to dataframe
for i in range(dfAIC.shape[0]):
    text_token = getTerms(str(dfAIC['Full Description'].iloc[i]))
    related_words = relatedSentences(text_token, target_token)
    dfAIC.at[i,'Word Match'] = int(related_words)

#Statistics
print("Minimum: " + str(np.min(dfAIC['Word Match'])))
print("Maximum: " + str(np.max(dfAIC['Word Match'])))
print("Average: " + str(np.average(dfAIC['Word Match'])))
print("Median: " + str(np.median(dfAIC['Word Match'])))
print("Standard deviation: " + str(np.std(dfAIC['Word Match'])))

#plot distribution with seaborn
sns.set(style="darkgrid")
sns.distplot(dfAIC['Word Match'])
plt.show()