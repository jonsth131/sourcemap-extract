#!/usr/bin/env python3
import json
import argparse
import os


def normalize_path(path):
    path = path.replace('webpack://', '')
    path = path.replace('../', '')
    path = path.replace('./', '')
    return os.path.normcase(path)


def process_sources(sources, sources_content, output_dir):
    for i, source in enumerate(sources):
        content = sources_content[i]

        if not content:
            print('[!] Empty file: ', source)
            continue

        path = normalize_path(source)
        print('[+] Saving file: ', path)

        os.makedirs(os.path.dirname(
            os.path.join(output_dir, path)), exist_ok=True)
        with open(os.path.join(output_dir, path), 'w') as f:
            f.write(content)


def process_sources_content(sources_content):
    for source_content in sources_content:
        print(source_content)


def process_sourcemap(sourcemap, output_dir):
    with open(sourcemap) as f:
        data = json.load(f)
    process_sources(data['sources'], data['sourcesContent'], output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sourcemap')
    parser.add_argument('--file', '-f', metavar='<FILE>', type=str,
                        help='sourcemap file', required=True)
    parser.add_argument('--output', '-o', metavar='<DIR>', type=str,
                        help='output directory', required=True)

    args = parser.parse_args()

    print(f'[+] Processing sourcemap file: {args.file}')
    process_sourcemap(args.file, args.output)
