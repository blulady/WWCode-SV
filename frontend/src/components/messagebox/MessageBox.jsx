import React from "react";

import styles from "./MessageBox.module.css";
import cx from "classnames";

const MessageBox = ({type, title, message, children}) => {
  const types = {
    Info: "Info",
    Success: "Success",
    Error: "Error",
  };

  const getTypeStr = (str) => {
    return types[str] || this.types.Info;
  };

  return (
    <div
      className={cx(
        styles[getTypeStr(type).toLowerCase()],
        styles["message-box"],
        "d-flex align-items-center justify-content-center flex-column"
      )}
      data-testid="message-box"
    >
      <div className={styles["title"]}>{title}</div>

      <div className={styles["message"]}>{message}</div>

     {children}
    </div>
  );
};
export default MessageBox;
