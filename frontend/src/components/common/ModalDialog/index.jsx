import React from "react";
import { createPortal } from "react-dom";
import Modal from "./Modal";

const ModalDialog = ({
  id,
  title,
  text,
  onCancel = () => Promise.resolve(),
  onConfirm,
  children,
}) => {
  return (
    <>
      {React.cloneElement(children, {
        "data-bs-toggle": "modal",
        "data-bs-target": `#${id}`,
        onClick: (event) => {
          event.stopPropagation();
        },
      })}
      {createPortal(
        <Modal
          id={id}
          title={title}
          text={text}
          onCancel={onCancel}
          onConfirm={onConfirm}
        />,
        document.body
      )}
    </>
  );
};

export default ModalDialog;
