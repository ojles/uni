#include "cppfiles_component.h"

#include <QDirIterator>

CppFilesComponent::CppFilesComponent(QObject *parent) : QObject(parent)
{
}

void CppFilesComponent::updateFiles()
{
    QDirIterator dirIterator(_sourcePath, QStringList() << "*.cpp", QDir::Files, QDirIterator::Subdirectories);

    _files->clear();
    while (dirIterator.hasNext()) {
        QString fullPath = dirIterator.next();
        QString name = fullPath.mid(_sourcePath.size());
        if (name.size() > 0 && name.at(0) == '/') {
            name = name.mid(1);
        }
        CppFile cppFile(name, fullPath);
        _files->add(cppFile);
    }

    _undoStack->clear();
    emit filesChanged();
}

CppFileModel* CppFilesComponent::files()
{
    return _files;
}

void CppFilesComponent::checkAll(bool checked)
{
    _files->forEach([checked](CppFile& file) -> void {
        file.setIsChecked(checked);
    });
}

Q_INVOKABLE void CppFilesComponent::moveByIndex(int fileIndex)
{
    _undoStack->push(new MoveFileUndoCommand(_files, fileIndex, _destinationPath));
}

Q_INVOKABLE void CppFilesComponent::returnByIndex(int fileIndex)
{
    _undoStack->push(new ReturnFileUndoCommand(_files, fileIndex, _destinationPath));
}

void CppFilesComponent::moveChecked()
{
    std::vector<int> indices;
    for (int i = 0; i < _files->rowCount(); i++)
    {
        CppFile* file = _files->getAtIndex(i);
        if (file->isChecked())
        {
            indices.push_back(i);
        }
    }

    _undoStack->push(new MoveFileUndoCommand(_files, indices, _destinationPath));
}

void CppFilesComponent::returnChecked()
{
    std::vector<int> indices;
    for (int i = 0; i < _files->rowCount(); i++)
    {
        CppFile* file = _files->getAtIndex(i);
        if (file->isChecked())
        {
            indices.push_back(i);
        }
    }

    _undoStack->push(new ReturnFileUndoCommand(_files, indices, _destinationPath));
}

void CppFilesComponent::undo()
{
    if (_undoStack->canUndo())
    {
        _undoStack->undo();
    }
}
