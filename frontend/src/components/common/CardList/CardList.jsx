import React from "react";
import styles from "./CardList.module.css";
import ModalDialog from "../ModalDialog";

const CardList = ({ columns, data, actions }) => {
    const renderActionButtons = (id, data) => {
        let buttons = [];
        actions?.map((action, idx) => {
            buttons.push(action.render(id, data));
            if (idx < actions.length - 1) {
                // add a divider
                buttons.push(<div className={styles["divider"]} />);
            }
        });
        return (<div className="d-flex flex-column align-items-center gap-3">{buttons}</div>)
    };

    return (
        <>
            {
                data.map((record, rowIndex) => (
                    <div
                        className={styles["cardlist-card"] + " d-flex flex-column"}
                        key={rowIndex}
                    >
                        {actions &&
                            <div className={"align-self-end"}>
                                <ModalDialog
                                    id={`cardlistModal${rowIndex}`}
                                    contents={renderActionButtons(`cardlistModal${rowIndex}`, record)}
                                >
                                    <div className={styles["icon"] + " " + styles["more"]}></div>
                                </ModalDialog>
                            </div>
                        }
                        {columns.map((column, idx) => (
                            <div className={"d-flex " + styles["row"]} key={idx}>
                                <div className={styles["column"]}>{column.title}</div>
                                <div className={styles["column"] + " wwc-text-capitalize"}>
                                    {column.render
                                        ? column.render(record[column.dataIndex], record)
                                        : record[column.dataIndex]}
                                </div>
                            </div>
                        ))}
                    </div>
                ))
            }
        </>
    );
};

export default CardList;
