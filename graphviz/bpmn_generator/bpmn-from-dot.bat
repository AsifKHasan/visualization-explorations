:: yml->dot->image pipeline

:: usage
:: mindmap-from-yml.bat DOT [ENGINE] [FMT]

:: ENGINE may be one of following. "neato" is the default
::   dot        - hierarchical or layered drawings of directed graphs.
::   neato      - "spring model" layouts.
::   fdp        - Force-Directed Placement.
::   sfdp       - Scalable Force-Directed Placement.
::   circo      - circular layout.
::   twopi      - radial layout.
::   nop        - Pretty-print DOT graph file. Equivalent to nop1.
::   nop2       - Pretty-print DOT graph file, assuming positions already known.
::   osage      - draws clustered graphs.
::   patchwork  - draws map of clustered graph using a squarified treemap layout. 

:: FMT may be one of jpg/png/pdf/svg. "svg" is the default

@echo off

:: parameters
set DOT=%~1
set ENGINE=%~2
set FMT=%~3

:: dot -> FMT
:: get the actual yml name without path prefix
set token_string=%DOT%

:find_last_loop
for /F "tokens=1* delims=/" %%A in ( "%token_string%" ) do (
  set DOT_NAME=%%A
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

:: engine 
if "%ENGINE%"=="" (
  set ENGINE="dot"
)

echo processing %DOT_NAME% : [FMT=%FMT%] [ENGINE=%ENGINE%]

pushd .\out
dot -K%ENGINE% -T%FMT%%RENDERER% -o%DOT_NAME%.%ENGINE%.%FMT% ..\data\%DOT_NAME%.gv

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
