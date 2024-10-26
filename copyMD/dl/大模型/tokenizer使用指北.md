---
title: tokenizer使用指北
top: false
cover: false
toc: true
mathjax: true
date: 2024-10-26 15:27:31
password:
summary:
tags:
- pytorch
- tokenizer
- LLM
categories:
- 学术
---

# 背景

文本到向量需要有个中间层，用来将文本分词，然后将不同的文本编码为序号。

例如一个文本

`i am your father.`

就应该分词为四个单词，然后其中首位还应该加入首位token。

那么如果我们需要在文本中加入特殊的token作为上下文分割呢？





# 加入新的token词汇

举例codeT5的diff的分割加入新的词汇

```
from transformers import AutoTokenizer


REPLACE = '<REPLACE>'
REPLACE_OLD = '<REPLACE_OLD>'
REPLACE_NEW = '<REPLACE_NEW>'
REPLACE_END = '<REPLACE_END>'

INSERT = '<INSERT>'
INSERT_OLD = '<INSERT_OLD>'
INSERT_NEW = '<INSERT_NEW>'
INSERT_END = '<INSERT_END>'

DELETE = '<DELETE>'
DELETE_END = '<DELETE_END>'

KEEP = '<KEEP>'
KEEP_END = '<KEEP_END>'

tokenizer_T5_special_tokens = [REPLACE, REPLACE_OLD, REPLACE_NEW, REPLACE_END, INSERT, INSERT_OLD, INSERT_NEW, INSERT_END, DELETE, DELETE_END, KEEP, KEEP_END]


def get_default_tokenizer(model_name = "Salesforce/codet5-base", special_tokens = []):
# 加载 alesforce/codet5-base 分词器
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if special_tokens:
        tokenizer.add_special_tokens({
            "additional_special_tokens":special_tokens
        })
    return tokenizer
```



# 新加入的词汇的ids是多少呢。



在 CodeT5 的 tokenizer 中新增 special tokens 后，**这些 token 的 ID 通常会附加到现有 token 的 ID 列表的末尾，不会影响已有 token 的 ID 序号。**因此，之前的 token ID 应该保持不变，不会因为新增的 special tokens 而被重新分配。

```
from transformers import AutoTokenizer

# 假设使用的是 codet5 tokenizer
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-small")

# 打印现有的 vocab size
print("Vocab size before:", tokenizer.vocab_size)

# 新增 special tokens
new_tokens = {"additional_special_tokens": ["<NEW_TOKEN_1>", "<NEW_TOKEN_2>"]}
tokenizer.add_special_tokens(new_tokens)

# 打印新增后的 vocab size 和新增 token 的 ids
print("Vocab size after:", tokenizer.vocab_size)
print("New token ids:", tokenizer.convert_tokens_to_ids(["<NEW_TOKEN_1>", "<NEW_TOKEN_2>"]))
```

OUT:

```
(pt) liuwenlong@gpu6-labot:~/KKCMG$ python test.py
Vocab size before: 32100
Vocab size after: 32100
New token ids: [32100, 32101]
```

