:: gsheet->json->dot->png pipeline

@echo off

:: parameters
set DOCUMENT=%1
set WORKSHEET=%1

:: json-from-gsheet
pushd .\gsheet-to-json\src
.\json-from-gsheet.py --config "../conf/config.yml" --gsheet "%DOCUMENT%" --worksheet "%WORKSHEET%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: dot-from-json
pushd .\json-to-dot\src
.\dot-from-json.py --config "../conf/config.yml" --json "%WORKSHEET%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: dot -> png
pushd .\out

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
