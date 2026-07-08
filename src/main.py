import site_generation as sg
import sys


def main():
    source_dir = 'static'
    destination_dir = 'docs'
    content_dir = 'content'
    basepath = '/'
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    # sg.copy(source_dir, destination_dir, True)
    sg.copy_alt(source_dir, destination_dir)
    sg.generate_pages_recursive(content_dir, 'template.html',
                                destination_dir, basepath)


if __name__ == '__main__':
    main()
