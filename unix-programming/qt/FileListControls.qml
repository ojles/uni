import QtQuick 2.0
import QtQuick.Controls 1.4

Item {
    readonly property bool checkedAll: checkAllCheckBox.checked;

    property var cppFiles;
    property var destinationFolderSelector;

    height: 30
    CheckBox {
        id: checkAllCheckBox
        anchors.verticalCenter: parent.verticalCenter
        x: 15
        text: "Check all"
        onCheckedChanged: {
            cppFiles.checkAll(checked);
        }
    }
    Button {
        x: returnAllButton.x - width - 10
        anchors {
            verticalCenter: parent.verticalCenter
        }
        enabled: (destinationFolderSelector.folder != "" && cppFiles.files.rowCount() > 0)
        text: "Move"
        onClicked: {
            cppFiles.moveChecked();
        }
    }
    Button {
        id: returnAllButton
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        enabled: destinationFolderSelector.folder != ""
        text: "Return"
        onClicked: {
            cppFiles.returnChecked();
        }
    }
}

