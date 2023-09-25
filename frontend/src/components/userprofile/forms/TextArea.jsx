import React from "react";
import cx from "classnames";
import FormLabelField from "./FormLabelField";

const TextArea = ({ id, label, rows=10, value="", name="", onChange, readonly=false, required=false }) => {
  return (
    <FormLabelField id={id} label={label} readonly={readonly} required={required}>
        <textarea id={id} rows={rows} value={value} name={name} readOnly={readonly} className={cx({ "form-control": !readonly, "form-control-plaintext": readonly, "required": required })} onChange={onChange}></textarea>
    </FormLabelField>
  );
};

export default TextArea;