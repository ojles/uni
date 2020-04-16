#ifndef CPPFILESCOMPONENT_H
#define CPPFILESCOMPONENT_H

#include "filemodel.h"
#include "undostack_commands.h"

#include <QUndoStack>
#include <QVariant>

class CppFilesComponent : public QObject
{
    Q_OBJECT
    // TODO: change to QUrl
    Q_PROPERTY(QString sourcePath READ sourcePath WRITE setSourcePath NOTIFY sourcePathChanged)
    Q_PROPERTY(QString destinationPath READ destinationPath WRITE setDestinationPath NOTIFY destinationPathChanged)
    Q_PROPERTY(CppFileModel* files READ files NOTIFY filesChanged)

public:
    explicit CppFilesComponent(QObject *parent = nullptr);

    QString sourcePath()
    {
        return _sourcePath;
    }

    QString destinationPath()
    {
        return _destinationPath;
    }

    void setSourcePath(QString sourcePath)
    {
        _sourcePath = sourcePath;
        emit sourcePathChanged();
        updateFiles();
    }

    void setDestinationPath(QString destinationPath)
    {
        _destinationPath = destinationPath;
        emit destinationPathChanged();
    }

    CppFileModel* files();

    Q_INVOKABLE void checkAll(bool checked);

    Q_INVOKABLE void moveByIndex(int fileIndex);

    Q_INVOKABLE void returnByIndex(int fileIndex);

    Q_INVOKABLE void moveChecked();

    Q_INVOKABLE void returnChecked();

    Q_INVOKABLE void undo();

signals:
    void sourcePathChanged();

    void destinationPathChanged();

    void filesChanged();

private:
    void updateFiles();

    QString _sourcePath;
    QString _destinationPath;
    CppFileModel* _files = new CppFileModel();
    QUndoStack* _undoStack = new QUndoStack();
};

#endif // CPPFILESCOMPONENT_H
