import QtQuick 2.12
import Qt.labs.platform 1.1
import QtQuick.Controls 2.12

    Item {
    id: topItem
    readonly property var folderDialog: _folderDialog;
    property string prefix;
    property string folder;

    FolderDialog {
        id: _folderDialog
        onAccepted: {
            let _folder = _folderDialog.folder.toString().substring(7);
            folderPathText.text = _folder;
            topItem.folder = _folder;
        }
    }
    Text {
        id: folderPrefix
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
        text: prefix
    }
    Text {
        id: folderPathText
        anchors {
            left: folderPrefix.right
            right: openButton.left
            verticalCenter: parent.verticalCenter
        }
        leftPadding: 10
        rightPadding: 5
        text: ""
        font.bold: true
        elide: Text.ElideRight

        YellowToolTip {
            id: folderPathTextToolTip
            text: folderPathText.text
        }
        MouseArea {
            id: folderPathTextMouseArea
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                if (folderPathText.text != "") {
                    folderPathTextToolTip.visible = true;
                }
            }
            onExited: {
                folderPathTextToolTip.visible = false;
            }
        }
    }
    OldStyleButton {
        id: openButton
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        text: "Browse..."
        onClicked: {
            _folderDialog.open();
        }
    }
}
