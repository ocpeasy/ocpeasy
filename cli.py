import fire


def say_hello(name=''):
    return 'Hello {}!'.format(name)


if __name__ == '__main__':
  fire.Fire()