rmdir /s /q documentation
python -m pdoc --html -c hljs_style='atom-one-dark' -c show_inherited_members=True -c lunr_search="{'fuzziness': 1, 'index_docstrings': True}" %cd% -o %cd%\documentation