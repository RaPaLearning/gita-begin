from os import path
import re
import json
import enchant
spelling = enchant.Dict('en_US')

md_path = path.join('..', 'gita')


def toc_to_filenames(toc):
    filenames = re.findall(r"\[.*?\]\((.*?)\)$", toc, re.MULTILINE)
    return filenames


def spell_check(text):
    accepts = ['Sattva', 'Tamas', 'Om']
    for word in re.findall(r"[\w'\u2019\-]+",  text):
        if not spelling.check(word) and word not in accepts:
            print(f'**check spelling: {word}')


def md_to_annotations(mdtext, md_filename):
    annotations = {}
    note_contents = re.findall(r"<a name='([\w]+)'><\/a>\s>(.*?)$", mdtext, re.MULTILINE)
    annotations['note_ids'] = [c[0] for c in note_contents]
    for text in [c[1] for c in note_contents]:
        spell_check(text)
    annotations['notes'] = [{'note_id': c[0], 'text': c[1].strip(), 'file': md_filename} for c in note_contents]
    return annotations


def toc_md_to_filenames():
    with open(path.join(md_path, 'toc.md'), 'r') as toc_md_file:
        return toc_to_filenames(toc_md_file.read())


def mds_to_notes():
    filenames = toc_md_to_filenames()
    md_note_ids = []
    notes = []
    for md_filename in filenames:
        with open(path.join(md_path, md_filename), encoding="utf8") as mdfile:
            annotations = md_to_annotations(mdfile.read(), md_filename)
            md_note_ids.append({md_filename: annotations['note_ids']})
            notes.extend(annotations['notes'])
    return md_note_ids, notes


def mark_prior_next_note(md_note_ids):
    md_prior_next_notes = {}
    def link_in_seq(link_name, link_index, md_note_ids_seq):
        link = ''
        for md_notes in md_note_ids_seq:
            for md_filename, notes in md_notes.items():
                if md_filename not in md_prior_next_notes:
                    md_prior_next_notes[md_filename] = {}
                md_prior_next_notes[md_filename][link_name] = link
                if len(notes) > 0:
                    link = notes[link_index]
    link_in_seq('prior', -1, md_note_ids)
    link_in_seq('next', 0, reversed(md_note_ids))
    return md_prior_next_notes


if __name__ == '__main__':
    md_to_note_ids_compiled, notes_compiled = mds_to_notes()
    with open('md_to_note_ids_compiled.json', 'w', encoding="utf8") as md_notes_file:
        json.dump(md_to_note_ids_compiled, md_notes_file)
    with open('notes_compiled.json', 'w', encoding="utf8") as notes_file:
        json.dump(notes_compiled, notes_file)
    with open('md_prior_next_note.json', 'w', encoding="utf8") as prior_next_file:
        json.dump(mark_prior_next_note(md_to_note_ids_compiled), prior_next_file)
