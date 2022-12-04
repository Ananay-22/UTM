for %%I in (.) do set CurrentWorkingFolder=%%~nxI
if "%CurrentWorkingFolder%" == "scripts" (cd ..)

rmdir /s /q documentation
mkdir documentation
mkdir "documentation\uml\"
python -m py2puml UTM UTM > %cd%\documentation\uml\dcd.puml
python -m plantuml %cd%\documentation\uml\dcd.puml -o %cd%\documentation\uml -s http://www.plantuml.com/plantuml/svg/
copy documentation\uml\dcd.png documentation\uml\dcd.svg
del documentation\uml\dcd.png
python -m pdoc -c hljs_style='atom-one-dark' -c show_inherited_members=True -c lunr_search="{'fuzziness': 1, 'index_docstrings': True}" --html %cd%\UTM -o %cd%\documentation