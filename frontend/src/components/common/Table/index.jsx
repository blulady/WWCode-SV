import React from "react";
import cx from "classnames";

const GenericTable = ({ columns, data, tableClass }) => {
  return (
    <table className={cx('table', tableClass)}>
      <thead>
        <tr>
          {columns.map((column) => {
            return <th key={column.key}>{column.title}</th>;
          })}
        </tr>
      </thead>
      <tbody>
        {data.map((record, rowIndex) => (
          <tr key={rowIndex}>
            {columns.map((column) => (
              <td key={column.key}>
                {column.render
                  ? column.render(record[column.dataIndex], record)
                  : record[column.dataIndex]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default GenericTable;
