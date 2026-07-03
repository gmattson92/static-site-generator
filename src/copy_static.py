import os
import shutil


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
