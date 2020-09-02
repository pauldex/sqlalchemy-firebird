@echo off
pushd "%~dp0"

rem - Uses system twine
twine upload dist/*

if errorlevel 1 (
  echo.
  pause
)

popd
