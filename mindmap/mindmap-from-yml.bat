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

:: dot -> FMT
pushd .\out

set FMT=svg
set RENDERER=":cairo:cairo"
@REM set RENDERER=":svg:core"
set ENGINE=neato
dot -K%ENGINE% -T%FMT%%RENDERER% -o%YML%.%FMT% %YML%.gv


if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
