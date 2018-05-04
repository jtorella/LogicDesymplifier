from equivalencerules import CondEquiv
from equivalencerules import BoolEquiv
from logicobjects import Atom
from logicobjects import Sentence
import copy
import inspect


def runAll(sen):
    print('RunAll on sentence: ', sen)
    sentences = [sen]

    cond_equiv = inspect.getmembers(CondEquiv, predicate=inspect.isfunction)
    bool_equiv = inspect.getmembers(BoolEquiv, predicate=inspect.isfunction)

    for method in cond_equiv:
        result = method[1](sen)

        if result != sen and result is not None:
            sentences.append(result)

    for method in bool_equiv:
        result = method[1](sen)

        if result != sen and result is not None:
            sentences.append(result)

    print('Returning:')
    for sen in sentences:
        print('   ', sen)

    return sentences


def recurseRunAll(sen, max_steps):
    print('Working on sentence: ', sen)
    if sen.get_step_count() > max_steps:
        print('Too many steps! Returning...')
        return [sen]

    if type(sen) is Atom:
        return_val = runAll(sen)
        return return_val

    sentences = [sen]
    sen = copy.deepcopy(sen)

    left_sens = recurseRunAll(sen.left_sen, max_steps)
    right_sens = recurseRunAll(sen.right_sen, max_steps)
    print('Left sens: ', left_sens)
    print('Right sens: ', right_sens)

    for left_sen in left_sens:
        for right_sen in right_sens:
            new_sen = Sentence(left_sen, right_sen,
                               sen.oper, sen.get_negations(), sen.get_steps())

            if new_sen not in sentences and new_sen.get_step_count() <= max_steps:
                sentences.append(new_sen)

            new_sens = runAll(new_sen)

            for sentence in new_sens:
                print(sentence, ' has count of ', sentence.get_step_count())
                if sentence.get_step_count() <= max_steps:
                    sentences.append(sentence)

    return sentences
