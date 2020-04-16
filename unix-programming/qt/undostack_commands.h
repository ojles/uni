#ifndef UNDOSTACK_COMMANDS_H
#define UNDOSTACK_COMMANDS_H

#include "filemodel.h"
#include "sql_action_logger.h"

#include <QUndoStack>
#include <QFile>
#include <QFileInfo>

class MoveFileUndoCommand : public QUndoCommand
{
public:
    MoveFileUndoCommand(CppFileModel* fileModel, int fileIndex, QString destinationPath);

    MoveFileUndoCommand(CppFileModel* fileModel, std::vector<int> fileIndices, QString destinationPath);

    void redo() override;

    void undo() override;

private:
    CppFileModel* _fileModel;
    std::vector<int> _fileIndices;
    QString _destinationPath;
    SqlActionLogger _actionLogger;
};

class ReturnFileUndoCommand : public QUndoCommand
{
public:
    ReturnFileUndoCommand(CppFileModel* fileModel, int fileIndex, QString destinationPath);

    ReturnFileUndoCommand(CppFileModel* fileModel, std::vector<int> fileIndices, QString destinationPath);

    void redo() override;

    void undo() override;

private:
    CppFileModel* _fileModel;
    std::vector<int> _fileIndices;
    QString _destinationPath;
    SqlActionLogger _actionLogger;
};

#endif // UNDOSTACK_COMMANDS_H
