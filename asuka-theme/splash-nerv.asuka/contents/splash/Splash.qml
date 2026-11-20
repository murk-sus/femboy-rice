import QtQuick
import QtQuick.Window

Rectangle {
    id: root
    color: "#0a0304"
    property int stage

    onStageChanged: {
        if (stage == 1) {
            introAnimation.running = true;
        }
    }

    readonly property var messages: [
        "MAGI SYSTEM: BOOTING",
        "シンクロ開始 // SYNC START",
        "Synchronisation läuft...",
        "Синхронизация пилота...",
        "EVA-02: ACTIVATION",
        "Na los, Baka! Ich warte nicht!"
    ]

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Text {
            id: title
            text: "NERV"
            font.family: "Shippori Mincho B1"
            font.weight: Font.ExtraBold
            font.pixelSize: Math.round(root.height * 0.09)
            color: "#dc2630"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: frame.top
            anchors.bottomMargin: root.height * 0.02
        }

        Rectangle {
            id: frame
            width: Math.min(root.width * 0.5, 900)
            height: width * 9 / 16
            anchors.centerIn: parent
            color: "transparent"
            border.color: "#c81c26"
            border.width: 3
            clip: true

            AnimatedImage {
                anchors.fill: parent
                anchors.margins: 3
                source: "images/asuka.gif"
                fillMode: Image.PreserveAspectCrop
                playing: true
                smooth: true
            }
        }

        Text {
            id: pilot
            text: "PILOT: 惣流・アスカ・ラングレー  //  EVA-02"
            font.family: "Oswald"
            font.pixelSize: Math.round(root.height * 0.022)
            color: "#ff6a13"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: frame.bottom
            anchors.topMargin: root.height * 0.025
        }

        Rectangle {
            id: barBg
            width: frame.width
            height: 6
            color: "#2a0a0c"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: pilot.bottom
            anchors.topMargin: root.height * 0.02
            Rectangle {
                height: parent.height
                width: parent.width * Math.min(1, root.stage / 6)
                color: "#dc2630"
                Behavior on width { NumberAnimation { duration: 400; easing.type: Easing.OutQuad } }
            }
        }

        Text {
            text: root.messages[Math.max(0, Math.min(root.messages.length - 1, root.stage - 1))]
                  + "   " + Math.round(Math.min(1, root.stage / 6) * 400) + "%"
            font.family: "Oswald"
            font.pixelSize: Math.round(root.height * 0.018)
            color: "#967064"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: barBg.bottom
            anchors.topMargin: root.height * 0.012
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: 600
        easing.type: Easing.InOutQuad
    }
}
