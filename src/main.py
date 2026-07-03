import site_generation as sg


def main():
    source_dir = 'static'
    destination_dir = 'public'
    # sg.copy(source_dir, destination_dir, True)
    sg.copy_alt(source_dir, destination_dir)

    sg.generate_page('content/index.md', 'template.html', 'public/index.html')

    sg.generate_page('content/blog/glorfindel/index.md', 'template.html',
                     'public/blog/glorfindel/index.html')
    sg.generate_page('content/blog/tom/index.md', 'template.html',
                     'public/blog/tom/index.html')
    sg.generate_page('content/blog/majesty/index.md', 'template.html',
                     'public/blog/majesty/index.html')
    sg.generate_page('content/contact/index.md', 'template.html',
                     'public/contact/index.html')


if __name__ == '__main__':
    main()
