:: bpmn->yml->svg image pipeline

:: usage
:: svg-from-bpmn.bat YML

@echo off

:: parameters
set BPMN=%~1

:: bpmn-to-yml
pushd .\bpmn-to-yml\src
.\yml-from-bpmn.py --config "../conf/config.yml" --bpmn "%BPMN%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd

:: yml-to-svg
pushd .\yml-to-svg\src
.\svg-from-yml.py --config "../conf/config.yml" --yml "%BPMN%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
