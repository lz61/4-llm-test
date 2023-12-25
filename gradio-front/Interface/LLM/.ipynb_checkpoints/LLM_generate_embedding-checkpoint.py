from modelscope.utils.constant import Tasks
from modelscope.pipelines import pipeline

import torch

# 文本向量模型
sentence_embedding_model = 'damo/nlp_corom_sentence-embedding_chinese-base'
pipeline_se = pipeline(Tasks.sentence_embedding, model=sentence_embedding_model)

def generate_embedding(text_list):
    with torch.no_grad():
        embs = pipeline_se(input={'source_sentence': text_list})['text_embedding']
    return embs