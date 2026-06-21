class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Arguments:
            tag - string representing the HTML tag name, e.g. "p" or "a"
                    (if None, value will render as plain text)
            value - string that goes in between the opening and closing
                    (if None, node is assumed to have children)
            children - list of HTMLNode children of this node
                    (if None, node is assumed to have a value)
            props - dict holding attributes of the tag
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        s = f'(tag={self.tag}, value={self.value}, children={self.children}, '
        s += f'props={self.props}'
        return s

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''
        html_str = ''
        for key, val in self.props.items():
            html_str += f' {key}="{val}"'
        return html_str


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self):
        s = f'(tag={self.tag}, value={self.value}, props={self.props}'
        return s

    def to_html(self):
        if self.tag == 'img':
            return self._img_to_html()
        if not self.value:
            raise ValueError('Non-image LeafNode must have non-empty value; '
                             f'this={self}')
        if not self.tag:
            return self.value
        opening = f'<{self.tag}{self.props_to_html()}>'
        closing = f'</{self.tag}>'
        return opening + self.value + closing

    def _img_to_html(self):
        if self.tag != 'img':
            raise ValueError('_img_to_html called on non-image node; '
                             f'this={self}')
        return f'<{self.tag}{self.props_to_html()}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __repr__(self):
        s = f'(tag={self.tag}, children={self.children}, props={self.props}'
        return s

    def to_html(self):
        if not self.tag:
            raise ValueError('ParentNode must have a tag; '
                             f'this={self}')
        if not self.children:
            raise ValueError('ParentNode must have children; '
                             f'this={self}')
        opening = f'<{self.tag}{self.props_to_html()}>'
        closing = f'</{self.tag}>'
        contents = ''
        for child in self.children:
            contents += child.to_html()
        return opening + contents + closing
