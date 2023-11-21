:: yml->dot->bpmn image pipeline

:: usage
:: bpmn-from-yml.bat YML [DIR]

:: DIR may be LR or TB. "LR" is the default

@echo off

:: parameters
set YML=%~1
set DIR=%~2

:: DIR
if "%DIR%"=="" (
  set DIR="LR"
) else if not "%DIR%"=="LR" if not "%DIR%"=="TB" (
  set DIR="LR"
)

:: yml-to-bpmn
pushd .\src
python yml-to-bpmn.py --config "../conf/config.yml" --yml "%YML%" --dir "%DIR%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: dot -> SVG
:: get the actual yml name without path prefix
set token_string=%YML%

:find_last_loop
for /F "tokens=1* delims=/" %%A in ( "%token_string%" ) do (
  set YML_NAME=%%A
  set token_string=%%B
  goto find_last_loop
)

echo processing %YML_NAME% : [DIR=%DIR%]

pushd .\out
dot -Kdot -Tsvg -o%YML_NAME%.svg %YML_NAME%.gv

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: post process SVG
echo post processing %YML_NAME%.svg : [DIR=%DIR%]

pushd .\src
python svg-post-process.py --config "../conf/config.yml" --svg "%YML_NAME%".svg --dir "%DIR%"

popd
