#ifndef FILEMODEL_H
#define FILEMODEL_H

#include <QObject>
#include <QAbstractListModel>

class CppFile : public QObject
{
    Q_OBJECT

public:
    enum FileStatus
    {
        NotChanged,
        Moved,
        Error
    };

    CppFile(const QString relativePath, const QString fullPath);

    CppFile(const CppFile& other);

    QString relativePath() const
    {
        return _relativePath;
    }

    QString fullPath() const
    {
        return _fullPath;
    }

    bool isChecked() const
    {
        return _isChecked;
    }

    FileStatus status() const
    {
        return _status;
    }

    void setIsChecked(bool isChecked)
    {
        _isChecked = isChecked;
    }

    void setStatus(FileStatus status)
    {
        _status = status;
    }

    CppFile& operator=(const CppFile& other);

signals:
    void relativePathChanged();

    void isCheckedChanged();

private:
    QString _relativePath;
    QString _fullPath;
    bool _isChecked;
    FileStatus _status;
};

class CppFileModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum FileRole
    {
        RelativePath = Qt::UserRole + 1,
        FullPath,
        IsChecked,
        Status
    };

    CppFileModel(QObject* parent = nullptr);

    void add(CppFile& cppFile);

    void clear();

    int rowCount(const QModelIndex & parent = QModelIndex()) const;

    QVariant data(const QModelIndex & index, int role = Qt::DisplayRole) const;

    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole);

    CppFileModel& operator=(const CppFileModel& other);

    void forEach(std::function<void (CppFile&)> func);

    CppFile* getAtIndex(int i);

    void applyAtIndex(int i, std::function<void (CppFile&)> func);

protected:
    QHash<int, QByteArray> roleNames() const;

private:
    QList<CppFile> _files;
};

#endif // FILEMODEL_H
