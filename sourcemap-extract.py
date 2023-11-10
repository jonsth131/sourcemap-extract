#!/usr/bin/env python3
import json
import argparse
import os
import requests


def normalize_path(path):
    path = path.replace('webpack://', '')
    path = path.replace('../', '')
    path = path.replace('./', '')
    return os.path.normcase(path)


def process_sources(sources, sources_content, output_dir):
    for i, source in enumerate(sources):
        content = sources_content[i]

        if not content:
            print('[!] Empty file:', source)
            continue

        path = normalize_path(source)
        print('[+] Saving file:', path)

        os.makedirs(os.path.dirname(
            os.path.join(output_dir, path)), exist_ok=True)
        with open(os.path.join(output_dir, path), 'w') as f:
            f.write(content)


def download_sourcemap(session, url, output_dir):
    try:
        r = session.get(url)
    except:
        return

    if r.status_code != 200:
        return

    return r.json()


def get_sourcemap_url_from_js(session, url):
    try:
        r = session.get(url)
    except:
        return

    if r.status_code != 200:
        return

    for line in r.text.splitlines():
        if 'sourceMappingURL' in line:
            base_url = url.rsplit('/', 1)[0]
            return base_url + '/' + line.split('sourceMappingURL=')[1]


def get_sourcemap_url(s, url):
    ext = url.split('.')[-1]
    if ext == 'js':
        return get_sourcemap_url_from_js(s, url)
    elif ext != 'map':
        return None
    return url


def download_sourcemaps_from_url_file(url_file, output_dir):
    s = requests.Session()
    with open(url_file) as f:
        for line in f:
            url = line.strip()
            url = get_sourcemap_url(s, url)
            if not url:
                continue

            print(f'[+] Downloading sourcemap from url: {url}')
            data = download_sourcemap(s, url, output_dir)
            if not data:
                print('[!] Failed to download sourcemap')
                continue

            process_sources(data['sources'],
                            data['sourcesContent'], output_dir)


def process_sourcemap(sourcemap, output_dir):
    with open(sourcemap) as f:
        data = json.load(f)
    process_sources(data['sources'], data['sourcesContent'], output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sourcemap')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', metavar='<FILE>', type=str,
                       help='sourcemap file', required=False)
    group.add_argument('--urls', '-u', metavar='<FILE>', type=str,
                       help='file containing sourcemap urls', required=False)
    parser.add_argument('--output', '-o', metavar='<DIR>', type=str,
                        help='output directory', required=True)

    args = parser.parse_args()

    if args.urls:
        print(f'[+] Processing sourcemap urls from file: {args.urls}')
        download_sourcemaps_from_url_file(args.urls, args.output)
    else:
        print(f'[+] Processing sourcemap file: {args.file}')
        process_sourcemap(args.file, args.output)
