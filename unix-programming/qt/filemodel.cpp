#include "filemodel.h"

CppFile::CppFile(const QString relativePath, const QString fullPath)
    : _relativePath(relativePath),
      _fullPath(fullPath),
      _isChecked(false),
      _status(FileStatus::NotChanged)
{
}

CppFile::CppFile(const CppFile& other)
{
    _relativePath = other._relativePath;
    _fullPath = other._fullPath;
    _isChecked = other._isChecked;
    _status = other._status;
}

CppFile& CppFile::operator=(const CppFile& other)
{
    _relativePath = other._relativePath;
    _fullPath = other._fullPath;
    _isChecked = other._isChecked;
    _status = other._status;
    return *this;
}

CppFileModel::CppFileModel(QObject* parent) : QAbstractListModel(parent)
{
}

void CppFileModel::add(CppFile& cppFile)
{
    beginInsertRows(QModelIndex(), rowCount(), rowCount());
    _files << cppFile;
    endInsertRows();
}

void CppFileModel::clear()
{
    beginRemoveRows(QModelIndex(), 0, rowCount() - 1);
    _files.clear();
    endRemoveRows();
}

int CppFileModel::rowCount(const QModelIndex & parent) const
{
    Q_UNUSED(parent)
    return _files.count();
}

QVariant CppFileModel::data(const QModelIndex & index, int role) const
{
    if (index.row() < 0 || index.row() >= _files.count())
    {
        return QVariant();
    }

    const CppFile& cppFile = _files[index.row()];
    if (role == RelativePath)
    {
        return cppFile.relativePath();
    }
    if (role == FullPath)
    {
        return cppFile.fullPath();
    }
    if (role == IsChecked)
    {
        return cppFile.isChecked();
    }
    if (role == Status)
    {
        return cppFile.status();
    }
    return QVariant();
}

bool CppFileModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (index.row() < 0 || index.row() >= _files.count())
    {
        return false;
    }

    CppFile& cppFile = _files[index.row()];
    if (role == IsChecked)
    {
        cppFile.setIsChecked(value.toBool());
        return true;
    }
    return false;
}

CppFileModel& CppFileModel::operator=(const CppFileModel &other)
{
    _files = other._files;
    return *this;
}

void CppFileModel::forEach(std::function<void (CppFile&)> func)
{
    for (int i = 0; i < _files.count(); i++) {
        func(_files[i]);
    }
    dataChanged(index(0), index(_files.count() - 1));
}

CppFile* CppFileModel::getAtIndex(int i)
{
    return &_files[i];
}

void CppFileModel::applyAtIndex(int i, std::function<void (CppFile&)> func)
{
    func(_files[i]);
    dataChanged(index(i), index(i));
}

QHash<int, QByteArray> CppFileModel::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[RelativePath] = "relativePath";
    roles[FullPath] = "fullPath";
    roles[IsChecked] = "isChecked";
    roles[Status] = "status";
    return roles;
}
