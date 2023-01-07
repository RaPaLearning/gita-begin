import unittest
from os import path
from compile_notes import toc_to_filenames, md_to_annotations, mds_to_notes, md_path


class CompileNotesTest(unittest.TestCase):
    def test_toc_to_filenames(self):
        filenames = toc_to_filenames('''
# Table of Contents

[Back to Basics](Back-to-Basics.md)

[Chapter 1](Chapter 1.md)

[1-1 to 1-11](1-1 to 1-11.md)

[4-30 (cont.) to 4-31](4-30 (cont.) to 4-31.md)
''')
        self.assertEqual(len(filenames), 4)
        self.assertEqual(filenames[0], 'Back-to-Basics.md')
        self.assertEqual(filenames[1], 'Chapter 1.md')
        self.assertEqual(filenames[2], '1-1 to 1-11.md')
        self.assertEqual(filenames[3], '4-30 (cont.) to 4-31.md')

    def test_md_note_to_annotations(self):
        annotations = md_to_annotations('''
This one has a full-stop

<a name='applnote_13'></a>
> We often doubt and worry.

The next one a comma

<a name='applnote_14'></a>
> In our anxiety, we interpret anything that happens as a signal of doom.

Here is an apostrophe

<a name='applnote_10'></a>
> Look beyond desire. Focus on the purpose even when you don’t reach the goal you expect.

''')
        self.assertEqual(len(annotations['note_ids']), 3)
        self.assertEqual(annotations['note_ids'][0], 'applnote_13')
        self.assertEqual(annotations['note_ids'][1], 'applnote_14')
        self.assertEqual(len(annotations['notes']), 3)
        self.assertEqual(annotations['notes'][0]['note_id'], 'applnote_13')
        self.assertEqual(annotations['notes'][0]['text'], 'We often doubt and worry.')
        self.assertEqual(annotations['notes'][1]['note_id'], 'applnote_14')
        self.assertEqual(annotations['notes'][1]['text'], 'In our anxiety, we interpret anything that happens as a signal of doom')
        self.assertEqual(annotations['notes'][2]['text'], 'Look beyond desire. Focus on the purpose even when you don’t reach the goal you expect.')
    def test_md_opener_to_annotation(self):
        annotation = md_to_annotations('''
in the journey of inquiry and don't get anxious about answers.

<a name='applopener_1'></a>
> Who am I?

## आत्म [Atma] - The Self''')
        self.assertEqual(len(annotation['note_ids']), 1)
        self.assertEqual(annotation['note_ids'][0], 'applopener_1')
        self.assertEqual(annotation['notes'][0]['note_id'], 'applopener_1')
        self.assertEqual(annotation['notes'][0]['text'], 'Who am I?')

    def test_gita_mds_to_annotations(self):
        def md_file_in_line(line):
            line = line.strip()
            return 1 if len(line) > 0 and '.md' in line else 0
        md_note_ids, notes = mds_to_notes()
        with open(path.join(md_path, 'toc.md'), 'r', encoding="utf8") as toc_file:
            md_file_count = sum([md_file_in_line(line) for line in toc_file])
        self.assertEqual(len(md_note_ids), md_file_count)
        self.assertGreater(len(notes), 200)


unittest.main()
