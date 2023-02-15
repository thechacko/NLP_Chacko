import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel


MODEL_PATH = './models/ldamodel'
NTOPICS = 10
RANDOM_STATE = 42
CHUNKSIZE = 1000
PASSES = 5

# Text Processing
data_lemmatized = [] # list of lemmatized data

# Model data Preparation
id2word = corpora.Dictionary(data_lemmatized)
corpus = [id2word.doc2bow(text) for text in data_lemmatized]

# Model building
lda_model_params = {
    'corpus':corpus,
    'id2word':id2word,
    'num_topics':NTOPICS, 
    'random_state':RANDOM_STATE,
    'chunksize':CHUNKSIZE,
    'passes':PASSES,
    'alpha':'auto',
    'per_word_topics':True,
    'update_every':1,
    }

lda_model = LdaModel(**lda_model_params)

# Fitting
doc_lda = lda_model[corpus]
lda_model.save(MODEL_PATH) # save model

# Prediction
saved_lda_model = LdaModel.load(MODEL_PATH) # load model
top_topics = model.top_topics(corpus)

# Evaluation
perplexity = lda_model.log_perplexity(corpus)

coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence = coherence_model_lda.get_coherence()

print("Perplexity score: ", perplexity)
print("Coherence score: ", coherence)
