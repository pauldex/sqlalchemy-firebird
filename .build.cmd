@echo off
pushd "%~dp0"

if exist dist\ (del /q dist\*.*)

rem - Uses system Python
python setup.py sdist bdist_wheel

if errorlevel 1 (
  echo.
  pause
)

popd
exit