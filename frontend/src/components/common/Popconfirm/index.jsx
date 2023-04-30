import React, { useState } from "react";

import styles from "./index.module.css";

const PopupConfirm = ({
  title,
  description,
  okText = "confirm",
  cancelText = "cancel",
  onConfirm,
  onCancel,
  children,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleCancel = () => {
    onCancel();
    setIsOpen(false);
  };

  const handleConfirm = () => {
    onConfirm();
    setIsOpen(false);
  };
  return (
    <>
      <button onClick={() => setIsOpen(true)}>{children}</button>

      {isOpen && (
        <div className={styles.popupConfirm}>
          <div className={styles.container}>
            <div className={styles.messageContainer}>
              <div className={styles.title}>{title}</div>
              <div className={styles.description}>{description}</div>
              <div className={styles.buttons}>
                <button className={styles.cancelButton} onClick={handleCancel}>
                  {cancelText}
                </button>
                <button
                  className={styles.confirmButton}
                  onClick={handleConfirm}
                >
                  {okText}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PopupConfirm;
