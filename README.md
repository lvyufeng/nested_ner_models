# 嵌套命名实体识别模型合集

由于项目和研究需要，要从论文（目前主要为计算机领域）中提取具有高度嵌套或复合名词的命名实体，传统Bi-LSTM+CRF在自建数据集的F1仅有60%左右。（虽然数据集标注的也有些问题）

下面根据近两年ArXiv和ACL出现过的Nested NER论文进行复现，看一下在自建数据集上的性能如何。

## 自建数据集
1. 共来自于CCF旗下13个刊物

1. 由CNKI抓取，仅包含论文摘要（全文有版权问题）

1. 目前仅标注了6000余条数据，后续重新标注后公开

## Nested NER 论文

1. [A Neural Layered Model for Nested Named Entity Recognition](https://github.com/meizhiju/layered-bilstm-crf) NAACL 2018

1. [Merge and Label: A novel neural network architecture for nested NER](https://github.com/fishjh2/merge_label) ACL2019
