from readers import cr
import sys
from torchtext import data
from torchtext import datasets
from torchtext.data import Field,BucketIterator
import torch

INPUTS = Field(init_token='<sos>',eos_token='<eos>', lower=True, batch_first=False)
ANSWERS = Field(sequential=True,tokenize=None, unk_token=None, is_target=True)
train_data, valid_data, test_data = cr.CR.splits(
            text_field=INPUTS, label_field=ANSWERS)
INPUTS.build_vocab(train_data)
ANSWERS.build_vocab(train_data)

train_iterator, valid_iterator, test_iterator = data.BucketIterator.splits(
            (train_data, valid_data, test_data), batch_size=8, device= torch.device('cuda') )
train_iterator.init_epoch()
for i, batch in enumerate(train_iterator):
    print(batch)
print(train_data)
