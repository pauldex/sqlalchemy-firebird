@echo off
pushd "%~dp0"

rem - Uses system twine
twine upload --repository testpypi dist/*

if errorlevel 1 (
  echo.
  pause
)

popd
exit