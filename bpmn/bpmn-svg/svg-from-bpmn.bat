:: bpmn->yml->svg image pipeline

:: usage
:: svg-from-bpmn.bat YML

@echo off

:: parameters
set BPMN=%~1

:: bpmn-to-yml
pushd .\bpmn-to-yml\src
@REM .\yml-from-bpmn.py --config "../conf/config.yml" --bpmn "%BPMN%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: get the actual yml name without path prefix
set token_string=%BPMN%

:find_last_loop
for /F "tokens=1* delims=/" %%A in ( "%token_string%" ) do (
  set YML_NAME=%%A
  set token_string=%%B
  goto find_last_loop
)

:: yml-to-svg
pushd .\yml-to-svg\src
.\svg-from-yml.py --config "../conf/config.yml" --yml "%YML_NAME%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
