:: yml->dot->png pipeline

@echo off

:: parameters
set YML=%1

:: yml-to-mindmap
pushd .\src
.\yml-to-mindmap.py --config "../conf/config.yml" --yml "%YML%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: dot -> png
pushd .\out

set FMT=png
set ENGINE=neato
dot -K%ENGINE% -T%FMT% -o%YML%.%FMT% %YML%.gv


if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
