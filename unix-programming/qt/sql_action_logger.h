#ifndef SQLACTIONLOGGER_H
#define SQLACTIONLOGGER_H

#include <QSql>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QVariant>
#include <QSqlError>

class SqlActionLogger
{
public:
    enum ActionType
    {
        Move,
        Return
    };

    SqlActionLogger();

    void log(ActionType actionType, QString source, QString destination);
};

#endif // SQLACTIONLOGGER_H
