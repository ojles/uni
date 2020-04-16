#include "undostack_commands.h"


QString combinePaths(QString a, QString b)
{
    QString result(a);
    if (result.back() != '/')
    {
        result.append("/");
    }
    result.append(b);
    return result;
}

void doMove(CppFile& file, QString destinationPath)
{
    if (file.status() == CppFile::FileStatus::Error || file.status() == CppFile::FileStatus::Moved)
    {
        return;
    }

    QFile qFile(file.fullPath());
    if (qFile.exists()) {
        QString destinationFilePath = combinePaths(destinationPath, QFileInfo(qFile).fileName());
        if (qFile.rename(destinationFilePath)) {
            file.setStatus(CppFile::FileStatus::Moved);
        } else {
            file.setStatus(CppFile::FileStatus::Error);
        }
    }
}

void doReturn(CppFile& file, QString destinationPath)
{
    if (file.status() == CppFile::FileStatus::Error || file.status() == CppFile::FileStatus::NotChanged)
    {
        return;
    }

    QString fileName = QFileInfo(QFile(file.fullPath())).fileName();
    QString filePath = combinePaths(destinationPath, fileName);
    QFile qFile(filePath);
    if (qFile.exists()) {
        if (qFile.rename(file.fullPath())) {
            file.setStatus(CppFile::FileStatus::NotChanged);
        } else {
            file.setStatus(CppFile::FileStatus::Error);
        }
    }
}

MoveFileUndoCommand::MoveFileUndoCommand(CppFileModel* fileModel, int fileIndex, QString destinationPath)
    : _fileModel(fileModel), _destinationPath(destinationPath)
{
    _fileIndices.push_back(fileIndex);
}

MoveFileUndoCommand::MoveFileUndoCommand(CppFileModel* fileModel, std::vector<int> fileIndices, QString destinationPath)
    : _fileModel(fileModel), _fileIndices(fileIndices), _destinationPath(destinationPath)
{
}

void MoveFileUndoCommand::redo()
{
    for (unsigned int i = 0; i < _fileIndices.size(); i++)
    {
        _fileModel->applyAtIndex(_fileIndices[i], [this](CppFile& file) -> void {
            doMove(file, _destinationPath);
            _actionLogger.log(SqlActionLogger::Move, file.fullPath(), _destinationPath);
        });
    }
}

void MoveFileUndoCommand::undo()
{
    for (unsigned int i = 0; i < _fileIndices.size(); i++)
    {
        _fileModel->applyAtIndex(_fileIndices[i], [this](CppFile& file) -> void {
            doReturn(file, _destinationPath);
            _actionLogger.log(SqlActionLogger::Return, file.fullPath(), _destinationPath);
        });
    }
}

ReturnFileUndoCommand::ReturnFileUndoCommand(CppFileModel* fileModel, int fileIndex, QString destinationPath)
    : _fileModel(fileModel), _destinationPath(destinationPath)
{
    _fileIndices.push_back(fileIndex);
}

ReturnFileUndoCommand::ReturnFileUndoCommand(CppFileModel* fileModel, std::vector<int> fileIndices, QString destinationPath)
    : _fileModel(fileModel), _fileIndices(fileIndices), _destinationPath(destinationPath)
{
}

void ReturnFileUndoCommand::redo()
{
    for (unsigned int i = 0; i < _fileIndices.size(); i++)
    {
        _fileModel->applyAtIndex(_fileIndices[i], [this](CppFile& file) -> void {
            doReturn(file, _destinationPath);
            _actionLogger.log(SqlActionLogger::Return, file.fullPath(), _destinationPath);
        });
    }
}

void ReturnFileUndoCommand::undo()
{
    for (unsigned int i = 0; i < _fileIndices.size(); i++)
    {
        _fileModel->applyAtIndex(_fileIndices[i], [this](CppFile& file) -> void {
            doMove(file, _destinationPath);
            _actionLogger.log(SqlActionLogger::Move, file.fullPath(), _destinationPath);
        });
    }
}
