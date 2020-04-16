import QtQuick 2.12
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.12

import lnu.oles.FirstTask 1.0

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    minimumWidth: 400
    minimumHeight: 350
    title: qsTr("First Task")

    menuBar: MenuBar {
        Menu {
            title: "&File"
            MenuItem {
                text: "Open &source folder..."
                onTriggered: {
                    sourceFolderSelector.folderDialog.open();
                }
            }
            MenuItem {
                text: "Open &destination folder..."
                onTriggered: {
                    destinationFolderSelector.folderDialog.open();
                }
            }
            MenuItem {
                text: "&Undo"
                shortcut: "Ctrl+Z"
                onTriggered: {
                    cppFiles.undo();
                }
            }
        }
        Menu {
            title: "&Help"
            MenuItem {
                text: "&About"
            }
        }
    }

    CppFiles {
        id: cppFiles
        sourcePath: sourceFolderSelector.folder;
        destinationPath: destinationFolderSelector.folder;
    }

    ColumnLayout {
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            bottom: parent.bottom
        }
        width: parent.width - 60
        spacing: 5

        FolderSelector {
            id: sourceFolderSelector
            Layout.fillWidth: true
            Layout.topMargin: 10
            height: 30
            prefix: "Source folder:"
        }

        FolderSelector {
            id: destinationFolderSelector
            Layout.fillWidth: true
            height: 30
            prefix: "Destination folder:"
        }

        FileListControls {
            id: fileListControls
            cppFiles: cppFiles
            destinationFolderSelector: destinationFolderSelector
            Layout.fillWidth: true
            Layout.topMargin: 20
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.bottomMargin: 20
            border {
                width: 1
                color: "#acacac"
            }

            StackLayout {
                id: stackLayout
                width: parent.width - 2
                height: parent.height - 2
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    verticalCenter: parent.verticalCenter
                }

                currentIndex: (sourceFolderSelector.folder == "")
                              ? 0
                              : (cppFiles.files.rowCount() <= 0)
                                    ? 1
                                    : 2

                RectangleWithMessage {
                    message: "Please select folder..."
                    onClickedCallback: function() {
                        sourceFolderSelector.folderDialog.open();
                    }
                }

                RectangleWithMessage {
                    message: "Empty folder, please select a different one..."
                    onClickedCallback: function() {
                        sourceFolderSelector.folderDialog.open();
                    }
                }

                FileList {
                    cppFiles: cppFiles
                    allChecked: fileListControls.checkedAll
                }
            }
        }
    }
}
