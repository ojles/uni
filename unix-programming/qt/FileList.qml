import QtQuick 2.0
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

ListView {
    property var cppFiles;
    property bool allChecked;

    model: cppFiles.files
    clip: true
    ScrollBar.vertical: ScrollBar {
        active: true
    }
    delegate: Rectangle {
        height: 35
        anchors.left: parent.left
        anchors.right: parent.right
        border {
            color: "#acacac"
            width: 1
        }
        color: "#fafafa"
        RowLayout {
            anchors.fill: parent
            OldStyleCheckBox {
                id: fileCheckBox
                Layout.alignment: Qt.AlignVCenter
                Layout.leftMargin: 15
                checked: isChecked
                onCheckedChanged: {
                    isChecked = checked;
                }
                Connections {
                    target: cppFiles.files
                    onDataChanged: {
                        fileCheckBox.checked = isChecked;
                    }
                }
                function trigger() {
                    checked = !checked;
                }
            }
            Text {
                id: folderPathText
                Layout.alignment: Qt.AlignVCenter
                Layout.fillWidth: true
                text: relativePath
                font {
                    pixelSize: 13
                }
                elide: Text.ElideRight

                YellowToolTip {
                    id: folderPathTextToolTip
                    text: parent.text
                }
                MouseArea {
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
            FileStatusMark {
                status: model.status
                Layout.leftMargin: 5
                Layout.rightMargin: 10
                Layout.alignment: Qt.AlignRight
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    fileCheckBox.trigger();
                }
            }
        }
    }
}
