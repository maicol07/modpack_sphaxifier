; CONSTANTS
#define AppName "Modpack Sphaxifier"
#define AppPublisher "Maicol07"
#define AppURL "https://maicol07.it"
#define AppExeName "main.exe"
;Version
#define VerFile FileOpen("VERSION")
#define AppVersion FileRead(VerFile)
#expr FileClose(VerFile)
#undef VerFile

[Setup]
AppId={{0767A424-BA1A-40C7-AC4F-FD61B59C9063}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={commonpf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=D:\Maicol\Documents\Progetti\Windows\Modpack_Sphaxifier\dist
OutputBaseFilename={#AppName} {#AppVersion} Setup
SetupIconFile=D:\Maicol\Documents\Progetti\Windows\Modpack_Sphaxifier\resources\img\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
AppCopyright=Copyright {#AppPublisher} © 2020
LicenseFile=LICENSE
UninstallDisplayName={#AppName}
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#AppPublisher}
VersionInfoTextVersion={#AppVersion}
VersionInfoCopyright=Copyright {#AppPublisher} © 2020
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AppVersion}
AppContact=maicolbattistini@live.it
AppReadmeFile=README.md
PrivilegesRequired=poweruser

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "D:\Maicol\Documents\Progetti\Windows\Modpack_Sphaxifier\dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "dist\main\*"; DestDir: "{app}"; Flags: createallsubdirs recursesubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
