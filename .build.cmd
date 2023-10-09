@echo off
pushd "%~dp0"

if exist dist\ (del /q dist\*.*)

python -m build

if errorlevel 1 (
  echo.
  pause
)

popd
exit