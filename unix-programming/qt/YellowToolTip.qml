import QtQuick 2.0
import QtQuick.Controls 2.12

ToolTip {
    id: toolTip
    delay: 500
    timeout: 5000
    contentItem: Text {
        text: toolTip.text
        wrapMode: Text.WrapAnywhere
    }
    background: Rectangle {
        color: "#fbf8eb"
        border {
            width: 1
            color: "black"
        }
        radius: 4
    }
}
