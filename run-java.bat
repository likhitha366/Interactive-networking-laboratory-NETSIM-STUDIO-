@echo off
setlocal
pushd "%~dp0"
set "PROJECT_JAVA_HOME=%~dp0.tooling\jdk\jdk-21.0.12.1+1"
if exist "%PROJECT_JAVA_HOME%\bin\javac.exe" set "JAVA_HOME=%PROJECT_JAVA_HOME%"
if not defined JAVA_HOME (
  echo Java Development Kit 21 is required. Install JDK 21 and set JAVA_HOME.
  popd
  exit /b 1
)
if not exist "%JAVA_HOME%\bin\javac.exe" (
  echo No Java compiler found at "%JAVA_HOME%\bin\javac.exe".
  echo Install JDK 21 or correct JAVA_HOME.
  popd
  exit /b 1
)
if not exist build mkdir build
"%JAVA_HOME%\bin\javac.exe" --add-modules jdk.httpserver -d build java\NetSimServer.java
if errorlevel 1 (
  echo Java compilation failed.
  popd
  exit /b 1
)
"%JAVA_HOME%\bin\java.exe" --add-modules jdk.httpserver -cp build NetSimServer
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%
