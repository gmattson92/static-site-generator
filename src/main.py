import site_generation as sg


def main():
    source_dir = 'static'
    destination_dir = 'public'
    content_dir = 'content'

    # sg.copy(source_dir, destination_dir, True)
    sg.copy_alt(source_dir, destination_dir)
    sg.generate_pages_recursive(content_dir, 'template.html', destination_dir)


if __name__ == '__main__':
    main()
