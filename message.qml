import QtQuick 1.0

Rectangle {
    signal messageRequired;

    function updateMessage(text) {
        messageText.text = text
    }

    anchors.fill: parent; color: "black"

    Text {
        id: messageText
        anchors.centerIn: parent; color: "white"
    }

    MouseArea {
        anchors.fill: parent
        onClicked: messageRequired()
    }
}