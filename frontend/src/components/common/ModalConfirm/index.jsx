import React, { useState, useEffect } from "react";

import styles from "./index.module.css";

const ModalConfirm = ({
  title,
  description,
  okText = "confirm",
  cancelText = "cancel",
  onConfirm,
  onCancel,
  children,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.classList.contains(styles.popupConfirm)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [])

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
      {React.cloneElement(children, {
        onClick: () => setIsOpen(true),
      })}

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

export default ModalConfirm;
