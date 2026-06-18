import textnode as tn


def main():
    dummy_node = tn.TextNode('This is some dummy text', tn.TextType.BOLD)
    print(dummy_node)


if __name__ == '__main__':
    main()
