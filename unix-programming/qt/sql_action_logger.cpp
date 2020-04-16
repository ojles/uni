#include "sql_action_logger.h"
#include <QDebug>

SqlActionLogger::SqlActionLogger()
{
}

void SqlActionLogger::log(ActionType actionType, QString source, QString destination)
{
    QSqlQuery query;
    query.prepare("insert into action (type, source, destination) values (:type, :source, :destination)");
    query.bindValue(":type", (actionType == Move) ? "MOVE" : "RETURN");
    query.bindValue(":source", source);
    query.bindValue(":destination", destination);
    if (!query.exec()) {
        qDebug() << "Failed to execute query";
        qDebug() << query.lastError();
    }
}
