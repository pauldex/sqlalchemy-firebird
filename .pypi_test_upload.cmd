@echo off
pushd "%~dp0"

twine upload --repository testpypi dist/*

if errorlevel 1 (
  echo.
  pause
)

popd
exit