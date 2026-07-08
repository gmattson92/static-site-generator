import os
import shutil
import glob
import markdown_parsing as mp


def clean_destination(target_dir: str, verbose=False) -> None:
    """
    Recursively removes a target directory, including all files and
    subdirectories.
    """
    if verbose:
        print('Entering clean_destination(): target_dir = '
              f'{target_dir}')
    if not (os.path.exists(target_dir)
            and os.path.isdir(target_dir)):
        print(f'clean_destination(): target_dir {target_dir} '
              'does not exist; done!')
        return

    contents = os.listdir(target_dir)
    paths = [os.path.join(target_dir, item) for item in contents]
    if verbose:
        print('Directory already exists; printing contents')
        for item in paths:
            print(item)

    # Remove files
    for item in paths:
        if os.path.isfile(item):
            if verbose:
                print(f'Removing file {item}...')
            os.remove(item)
        elif os.path.isdir(item):
            clean_destination(item, verbose)
        else:
            raise ValueError(f'Item {item} is not a file or directory; '
                             'doing nothing!')

    # Remove target_dir now that it's empty
    new_items = os.listdir(target_dir)
    if new_items:
        raise OSError(f'target_dir {target_dir} '
                      'should now be empty but isn\'t!')
    else:
        if verbose:
            print(f'Removing empty dir {target_dir}...')
        os.rmdir(target_dir)


def clean_destination_alt(target_dir):
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    else:
        print(f'clean_destination_alt(): target_dir {target_dir} is not a '
              'valid directory path; doing nothing!')


def copy(source_dir: str, target_dir: str, verbose=False) -> None:
    """
    Recursively copy all files and directories from source_dir to
    target_dir.
    """
    if verbose:
        print(f'Entering copy(): source_dir = {source_dir}, '
              f'target_dir = {target_dir}')
    # First make sure the source directory exists and is non-empty
    if not (os.path.exists(source_dir)
            and os.path.isdir(source_dir)):
        print(f'copy(): source_dir {source_dir} does not exist; done!')
        return
    if not os.listdir(source_dir):
        print(f'copy(): source_dir {source_dir} is empty; done!')
        return

    # If destination directory exists, delete the old contents
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        if verbose:
            print('Cleaning target directory...')
        clean_destination(target_dir, verbose)
    # (Re-)Create the destination directory
    if verbose:
        print('Recreating empty target directory...')
    os.mkdir(target_dir)

    # Copy all files
    src_contents = os.listdir(source_dir)
    src_paths = [os.path.join(source_dir, item) for item in src_contents]
    if verbose:
        print('Printing source_dir contents:')
        for item in src_paths:
            print(item)
    for item in src_paths:
        if os.path.isfile(item):
            if verbose:
                print(f'Copying file {item} to {target_dir}')
            shutil.copy(item, target_dir)
        elif os.path.isdir(item):
            copy(item,
                 os.path.join(target_dir, os.path.basename(item)),
                 verbose)
        else:
            raise ValueError(f'Item {item} is not a file or directory; '
                             'doing nothing!')


def copy_alt(source_dir, target_dir):
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    if os.path.exists(source_dir) and os.path.isdir(source_dir):
        shutil.copytree(source_dir, target_dir)


def change_basepath(html_str, new_basepath):
    old_link_str = 'href="/'
    new_link_str = f'href="{new_basepath}'
    old_img_str = 'src="/'
    new_img_str = f'src="{new_basepath}'
    links_replaced = html_str.replace(old_link_str, new_link_str)
    both_replaced = links_replaced.replace(old_img_str, new_img_str)
    return both_replaced


def generate_page(src_path, template_path, dst_path, basepath):
    print(f'Generating page from {src_path} to {dst_path} '
          f'using {template_path}')
    if not os.path.exists(src_path) or not os.path.isfile(src_path):
        raise ValueError(f'Source file {src_path} does not exist!')
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        raise ValueError(f'Template file {template_path} does not exist!')

    with open(src_path, 'r') as src_file:
        src_str = src_file.read()
    with open(template_path, 'r') as template_file:
        template_str = template_file.read()
    html_node = mp.markdown_to_htmlnode(src_str)
    html_str = html_node.to_html()
    title = mp.extract_title(src_str)
    # Replace '{{ Title }}' and '{{ Content }}' placeholders in template_str
    title_placeholder = '{{ Title }}'
    content_placeholder = '{{ Content }}'
    template_str = template_str.replace(title_placeholder, title)
    template_str = template_str.replace(content_placeholder, html_str)
    # Replace default "/" with basepath
    final_html_str = change_basepath(template_str, basepath)
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    with open(dst_path, 'w') as dst_file:
        dst_file.write(final_html_str)


def get_destination_path(md_path, src_dir_root, dst_dir_root):
    md_dir = os.path.dirname(md_path)
    dst_dir = md_dir.replace(src_dir_root, dst_dir_root)
    md_fname = os.path.basename(md_path)
    dst_fname = md_fname.replace('.md', '.html')
    dst_path = os.path.join(dst_dir, dst_fname)
    return dst_path


def mk_dst(html_path, verbose=False):
    html_dir = os.path.dirname(html_path)
    if os.path.exists(html_dir) and os.path.isdir(html_dir):
        return
    else:
        if verbose:
            print(f'Creating directory {html_dir} for output {html_path}')
        os.makedirs(html_dir)


def generate_pages_recursive(
    src_dir_path, template_path, dst_dir_root, basepath='/'
):
    """
    Generates the full website HTML and directory structure by generating HTML
    from source *.md files in src_dir_path and its subdirectories. Uses the
    template given by template_path. Generates HTML files under a mirrored
    directory structure with root basepath/dst_dir_root.
    """
    glob_str = os.path.join(src_dir_path, r'**/*.md')
    md_source_paths = glob.glob(glob_str, recursive=True)
    for md_source in md_source_paths:
        dst_path = get_destination_path(md_source, src_dir_path, dst_dir_root)
        mk_dst(dst_path, True)
        generate_page(md_source, template_path, dst_path, basepath)
