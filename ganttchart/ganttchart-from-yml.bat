:: yml->dot->ganttchart image pipeline

:: usage
:: ganttchart-from-yml.bat YML [FMT]

:: FMT may be one of jpg/png/pdf/svg. "svg" is the default

@echo off

:: parameters
set YML=%~1
set FMT=%~2

:: yml-to-ganttchart
pushd .\src
python yml-to-ganttchart.py --config "../conf/config.yml" --yml "%YML%"

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

:: format
if "%FMT%"=="" (
  set FMT=svg
  set RENDERER=":cairo:cairo"
) else if "%FMT%"=="svg" (
  set RENDERER=":cairo:cairo"
) else (
  set RENDERER=""
)

echo processing %YML_NAME% : [FMT=%FMT%]

pushd .\out
dot -Kdot -T%FMT%%RENDERER% -o%YML_NAME%.%FMT% %YML_NAME%.gv

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
