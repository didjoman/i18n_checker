import argparse
import fnmatch
import os
import re


def parseArguments():

    parser = argparse.ArgumentParser(description='Look for unused keywords in i18n file.')
    parser.add_argument('i18n_file', help='the path to the i18n file')
    parser.add_argument('target_directory', help='the path to the directory containing the files using the i18n keywords.')
    parser.add_argument('-e', '--extension', default='', help='the extention of the files using the i18n keywords.')

    return parser.parse_args()


def find_word_in_folder(word, folder_path, extension):

    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Search the word in the files of the current folder :
        for filename in fnmatch.filter(filenames, '*' + extension):
            file_path = os.path.join(dirpath, filename)
            word_found_in_file = find_word_in_file(word, file_path)
            if word_found_in_file:
                return True

        # If the word has not been found in the files of the current folder,
        # search it in the subforlders :
        for dirname in dirnames:
            dir_path = os.path.join(folder_path, dirname)
            word_found_in_folder = find_word_in_folder(word, dir_path, extension)
            if word_found_in_folder:
                return True
            
    # Word not found:
    return False
            

def find_word_in_file(word, file_path):
    with open(file_path, 'r') as f:
        for line in f:
            match_keyword = re.match('.*\#\{i18n\.' + word + '\}.*',line)
            if match_keyword:
                return True
            
    return False


def find_unused_keywords_of_i18nfile_in_folder(i18n_file_path, target_folder, extension):
    '''
    Walk through the i18n file and search each keyword in the files of the target directory:
    '''

    unused_keywords = []
    with open(i18n_file_path, 'r') as f:
        i = 1
        for line in f:
            match_keyword = re.match('\s*(\w*)\s*=.*',line)

            if match_keyword:
                keyword = match_keyword.group(1)
                i18n_keyword = '#{i18n.' + keyword + '}'  
                keyword_found = find_word_in_folder(keyword, target_folder, extension)
                if not keyword_found:
                    unused_keywords.append((i,keyword))
                    
            i += 1

    return unused_keywords


def format_table_entry(content):
    return '| ' + format(content, '76s') + ' |'


def format_table_keyword_entry(line, keyword):
    return format_table_entry(format(line, ' <5d') + ': ' + keyword)


def main():
    
    args = parseArguments()
    
    print('')
    print('Looking for unused keywords for the i18n file : "' + args.i18n_file + '" ...')
    print('')

    unused_keywords = find_unused_keywords_of_i18nfile_in_folder(args.i18n_file, args.target_directory, args.extension)

    if not unused_keywords:
        print('No unused keywords found.')
        print('')
        
    else:
        # display array of unused keywords : 
        print('-> ' + str(len(unused_keywords)) + ' keywords are unused in the '+ args.extension +' files of the target directory "' + args.target_directory + '":')
        print('-'*80)
        print('| ' + format('Line : keyword', '76s') + ' |')
        print('-'*80)
        for (line, keyword) in unused_keywords:
            print(format_table_keyword_entry(line, keyword))
        print('-'*80)
        print('')
    
        
# MAIN :             
main()
