@echo off
pushd "%~dp0"

twine upload dist/*

if errorlevel 1 (
  echo.
  pause
)

popd
exit
