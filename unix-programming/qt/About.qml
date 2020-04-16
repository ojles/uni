import QtQuick 2.0

Text {
    anchors.fill: parent
    textFormat: TextEdit.MarkdownText
    wrapMode: Text.WordWrap
    text: "
This program is not intended for any serious use.
It is just an university project.
You can find the source code <a href=\"https://github.com/ojles/uni/tree/unix/qt\" target=\"_blank\">here.</a>
<br/>
The task was to create an application that searches for *.cpp files
in the source folder and moves them to the destination folder. You can move each file separately or move the files that are checked.
<br/>
Also you can return the file if you would like.
Just press the 'Return' button on the file or at the top of the file list.
<br/>
I've also implemented QUndoStack so you can undo your changes by pressing Ctrl+Z.
<br/>
If you see a green check mark on the right that means the file has been moved successfully.
If a red 'x' appears that means an error occured.
It could be that such file already exists in the destination folder
or you don't have write permissions to the destination folder
or you deleted the file from source folder;
"
}
