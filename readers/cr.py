
from torchtext import data
# from torchtext.datasets.nli import ParsedTextField, ShiftReduceField
class CRDataset(data.TabularDataset):

    urls = []
    dirname = ''
    name = 'conversational_response'

    @staticmethod
    def sort_key(ex):
        return data.interleave_keys(
            len(ex.question))

    @classmethod
    def splits(cls, text_field, label_field, parse_field=None,
               extra_fields={}, root='.data', train='train.jsonl',
               validation='val.jsonl', test='test.jsonl'):
        """Create dataset objects for splits of the SNLI dataset.

        This is the most flexible way to use the dataset.

        Arguments:
            text_field: The field that will be used for premise and hypothesis
                data.
            label_field: The field that will be used for label data.
            parse_field: The field that will be used for shift-reduce parser
                transitions, or None to not include them.
            extra_fields: A dict[json_key: Tuple(field_name, Field)]
            root: The root directory that the dataset's zip archive will be
                expanded into.
            train: The filename of the train data. Default: 'train.jsonl'.
            validation: The filename of the validation data, or None to not
                load the validation set. Default: 'dev.jsonl'.
            test: The filename of the test data, or None to not load the test
                set. Default: 'test.jsonl'.
        """
        path = cls.download(root)

        if parse_field is None:
            fields = {'RelQuestion': ('question', text_field),
                      'comment0': ('comment0', text_field),
                      'comment1': ('comment1', text_field),
                      'comment2': ('comment2', text_field),
                      'comment3': ('comment3', text_field),
                      'comment4': ('comment4', text_field),
                      'comment5': ('comment5', text_field),
                      'comment6': ('comment6', text_field),
                      'comment7': ('comment7', text_field),
                      'comment8': ('comment8', text_field),
                      'comment9': ('comment9', text_field),
                      'RelScore': ('label', label_field)
                      }
        # else:
        #     fields = {'sentence1_binary_parse': [('premise', text_field),
        #                                          ('premise_transitions', parse_field)],
        #               'sentence2_binary_parse': [('hypothesis', text_field),
        #                                          ('hypothesis_transitions', parse_field)],
        #               'gold_label': ('label', label_field)}

        for key in extra_fields:
            if key not in fields.keys():
                fields[key] = extra_fields[key]
            else:
                new_field = [fields[key], extra_fields[key]]
                fields[key] = new_field

        return super(CRDataset, cls).splits(path, root, train, validation, test,
            format='json', fields=fields,
            filter_pred=lambda ex: ex.label != '-')

    @classmethod
    def iters(cls, batch_size=32, device=0, root='.data',
              vectors=None, trees=False, **kwargs):
        """Create iterator objects for splits of the SNLI dataset.

        This is the simplest way to use the dataset, and assumes common
        defaults for field, vocabulary, and iterator parameters.

        Arguments:
            batch_size: Batch size.
            device: Device to create batches on. Use -1 for CPU and None for
                the currently active GPU device.
            root: The root directory that the dataset's zip archive will be
                expanded into; therefore the directory in whose wikitext-2
                subdirectory the data files will be stored.
            vectors: one of the available pretrained vectors or a list with each
                element one of the available pretrained vectors (see Vocab.load_vectors)
            trees: Whether to include shift-reduce parser transitions.
                Default: False.
            Remaining keyword arguments: Passed to the splits method.
        """
        if trees:
            TEXT = ParsedTextField()
            TRANSITIONS = ShiftReduceField()
        else:
            TEXT = data.Field(tokenize='spacy')
            TRANSITIONS = None
        LABEL = data.Field(sequential=False)

        train, val, test = cls.splits(
            TEXT, LABEL, TRANSITIONS, root=root, **kwargs)

        TEXT.build_vocab(train, vectors=vectors)
        LABEL.build_vocab(train)

        return data.BucketIterator.splits(
            (train, val, test), batch_size=batch_size, device=device)


class CR(CRDataset):
    urls = []
    dirname = ''
    name = 'conversational_response'

    @classmethod
    def splits(cls, text_field, label_field, parse_field=None, root='.data', extra_fields={},
               train='train.jsonl', validation='dev.jsonl',
               test='test.jsonl'):
        return super(CR, cls).splits(text_field, label_field, parse_field=parse_field, extra_fields=extra_fields,
                                       root=root, train=train, validation=validation,
                                       test=test)


