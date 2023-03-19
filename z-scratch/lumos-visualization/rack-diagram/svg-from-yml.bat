:: yml->svg pipeline

@echo off

:: parameters
set YML=%1

:: yml-to-mindmap
pushd .\src
.\yml-to-svg.py --config "../conf/config.yml" --yml "%YML%"

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
