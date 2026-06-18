import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        node2 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        self.assertEqual(node1, node2)

    def test_neq1(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node', TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq3(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node', TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq4(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq5(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node',
                         TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq6(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node',
                         TextType.ITALIC, 'boot.dev')
        self.assertNotEqual(node1, node2)


if __name__ == '__main__':
    unittest.main()
