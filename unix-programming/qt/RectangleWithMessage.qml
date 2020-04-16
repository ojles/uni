import QtQuick 2.0

Rectangle {
    property var message;
    property var onClickedCallback;

    color: "#fafafa"

    Text {
        anchors {
            centerIn: parent
        }
        text: message
        color: "gray"
        font {
            pixelSize: 15
        }
    }
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            onClickedCallback();
        }
    }
}
