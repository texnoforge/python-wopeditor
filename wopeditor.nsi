!define NAME "Words of Power Editor"
!define REGPATH_UNINSTSUBKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${NAME}"
!define SHORTNAME "wopeditor"
; TODO: parse from wopeditor module
!define VERSION "0.2.0"
Name "${NAME}"
OutFile "dist\${SHORTNAME}-${VERSION}_installer.exe"
Unicode True
RequestExecutionLevel Admin ; Request admin rights on WinVista+ (when UAC is turned on)
InstallDir "$ProgramFiles\$(^Name)"
InstallDirRegKey HKLM "${REGPATH_UNINSTSUBKEY}" "UninstallString"

!include LogicLib.nsh
!include Integration.nsh

Page Directory
Page InstFiles

Uninstpage UninstConfirm
Uninstpage InstFiles


Section "Program files (Required)"
  SectionIn Ro

  SetOutPath $InstDir

  File /r "dist\wopeditor\*"
  WriteUninstaller "$InstDir\uninst.exe"
  WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "DisplayName" "${NAME}"
  WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "UninstallString" '"$InstDir\uninst.exe"'
  WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "NoModify" 1
  WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "NoRepair" 1

SectionEnd

Section "Start Menu shortcut"
  CreateShortcut /NoWorkingDir "$SMPrograms\${NAME}.lnk" "$InstDir\wopeditor.exe"
SectionEnd

Section -Uninstall
  ${UnpinShortcut} "$SMPrograms\${NAME}.lnk"
  Delete "$SMPrograms\${NAME}.lnk"

  RMDir /r "$InstDir"
  DeleteRegKey HKLM "${REGPATH_UNINSTSUBKEY}"
SectionEnd
