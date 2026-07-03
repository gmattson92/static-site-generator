import copy_static as cs


def main():
    source_dir = 'static'
    destination_dir = 'public'
    # cs.copy(source_dir, destination_dir, True)
    cs.copy_alt(source_dir, destination_dir)


if __name__ == '__main__':
    main()
