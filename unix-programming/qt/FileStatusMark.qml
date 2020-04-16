import QtQuick 2.0

Text {
    property int status;

    text: " "
    color: "green"
    font {
        pixelSize: 25
        family: "Monospace"
    }

    onStatusChanged: {
        if (status === 0) {
            text = " ";
        } else if (status === 1) {
            text = "✓";
            color = "green";
        } else {
            text = "✕";
            color = "red";
        }
    }
}
