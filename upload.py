#!/usr/bin/python

import requests, tempfile, sys, os
from variables import cookies, database_url
from multiprocessing import Pool
from lxml import html
from lxml.etree import tostring


def get_thing_information(database_url):
    print(database_url)
    response = requests.get(database_url, cookies = cookies)
    tree = html.fromstring(response.text)
    div_elements = tree.xpath("//tr[contains(@class, 'thing')]")
    entries = []
    for div in div_elements:
        thing_id = div.attrib['data-thing-id']
        try:
            word = div.xpath("td[2]/div/div/text()")[0]
            e = div.xpath("td[14]/div/div")[0]
            filename = e.text_content()
        except IndexError:
            print("failed to get the word of item with id " + str(thing_id) + ' on ' + str(database_url))
            continue
        audio_column_id = div.xpath("td[contains(@class, 'audio')]/@data-key")[0]
        audio_files = div.xpath("td[contains(@class, 'audio')]/div/div[contains(@class, 'dropdown-menu')]/div")
        num_audio_files = len(audio_files)

        entries.append({'thing_id': thing_id, 'num_audio_files': num_audio_files, \
                        'word': word, 'audio_column_id': audio_column_id, 'audio_filename': filename})

    return entries

def count_pages(database_url):
    raw_content = requests.get(database_url, cookies=cookies).content
    root = html.fromstring(raw_content)
    elements = root.xpath("//div[contains(@class, 'pagination')]/ul/li")
    if len(elements) <= 1:
        num_pages = 1
    else:
        num_pages = int(elements[-2].text_content())

    return num_pages

def get_database_information(database_url):
    num_pages = count_pages(database_url)

    page_urls = []
    for page in range(1, num_pages + 1):
        page_urls.append("%s?page=%s" % (database_url, str(page)))

    pool = Pool(processes = 8)
    entries = pool.map(get_thing_information, page_urls)

    return entries

def delete_word(thing_id):
    form_data = {
        "thing_id": thing_id,
        "csrfmiddlewaretoken": cookies['csrftoken']}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
        "referer": database_url}
    post_url = "https://www.memrise.com/ajax/thing/delete/"
    r = requests.post(post_url, cookies=cookies, headers=headers, data=form_data, timeout=60)

    return r.json()

def delete_database(database_url):
    page_entries = get_database_information(database_url)

    thing_ids = []
    for page_entry in page_entries:
        for entry in page_entry:
            thing_ids.append(entry['thing_id'])

    pool = Pool(processes = 8)
    results = pool.map(delete_word, thing_ids)

    print(results)

###########################################################

def upload_an_audio_file(entry):
    thing_id = entry['thing_id']
    cell_id = entry['audio_column_id']
    filename = entry['audio_filename']

    files = {'f': (filename, open(filename, 'rb'), 'audio/mp3')}
    form_data = {
        "thing_id": thing_id,
        "cell_id": cell_id,
        "cell_type": "column",
        "csrfmiddlewaretoken": cookies['csrftoken']}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
        "referer": entry['database_url']}
    post_url = "https://www.memrise.com/ajax/thing/cell/upload_file/"
    r = requests.post(post_url, files=files, cookies=cookies, headers=headers, data=form_data, timeout=60)

    return {"success": r.json()["success"]}

def upload_audio_files_to_database(database_url):
    page_entries = get_database_information(database_url)
    entries = []
    for page_entry in page_entries:
        for entry in page_entry:
            if (entry['num_audio_files'] == 0 and os.path.exists(entry['audio_filename']) and \
                    os.path.isfile(entry['audio_filename'])):
                entry['database_url'] = database_url
                entries.append(entry)

    pool = Pool(processes = 8)
    results = pool.map(upload_an_audio_file, entries)

    for result in results:
        print(result)

if __name__ == "__main__":
    #number_of_pages = count_pages(database_url)
    #get_audio_files_from_course(database_url, number_of_pages)
    #get_database_information(database_url)
    #delete_database(database_url)

    upload_audio_files_to_database(database_url)
