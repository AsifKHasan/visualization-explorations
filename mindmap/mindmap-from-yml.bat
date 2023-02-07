:: yml->dot->image pipeline

@echo off

:: parameters
set YML=%~1

:: yml-to-mindmap
pushd .\src
.\yml-to-mindmap.py --config "../conf/config.yml" --yml "%YML%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: dot -> FMT
:: get the actual yml name without path prefix
set token_string=%YML%

:find_last_loop
for /F "tokens=1* delims=/" %%A in ( "%token_string%" ) do (
  set YML_NAME=%%A
  set token_string=%%B
  goto find_last_loop
)

echo processing %YML_NAME%

pushd .\out

set FMT=svg
set RENDERER=":cairo:cairo"
@REM set RENDERER=":svg:core"
set ENGINE=neato
dot -K%ENGINE% -T%FMT%%RENDERER% -o%YML_NAME%.%FMT% %YML_NAME%.gv


if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
