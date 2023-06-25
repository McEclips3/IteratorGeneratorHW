import types


class FlatIterator:

    def __init__(self, n_list):
        self.n_list = iter(n_list)

    def __iter__(self):
        self.chunk = iter(next(self.n_list))
        return self

    def __next__(self):
        try:
            item = next(self.chunk)
        except StopIteration:
            try:
                self.chunk = iter(next(self.n_list))
                item = next(self.chunk)
            except StopIteration:
                raise StopIteration
        return item


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def flat_generator(n_list):
    for item in n_list:
        for x in item:
            yield x


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


class FlatIterator2:
    def __init__(self, list_of_list):
        self.list_of_list = list(reversed(list_of_list))

    def __iter__(self):
        return self

    def __next__(self):
        while self.list_of_list:
            self.chunk = self.list_of_list.pop()
            if type(self.chunk) is not list:
                return self.chunk
            else:
                for el in reversed(self.chunk):
                    self.list_of_list.append(el)

        raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    # for i in FlatIterator2(list_of_lists_2):
    #     print(i)


def flat_generator2(list_of_list):
    for i in list_of_list:
        if type(i) is list:
            yield from flat_generator2(i)
        else:
            yield i


def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)
    for i in flat_generator2(list_of_lists_2):
        print(i)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
